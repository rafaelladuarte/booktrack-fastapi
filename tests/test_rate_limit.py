import pytest
from http import HTTPStatus
from httpx import AsyncClient

from booktrack_fastapi.models.users import User
from booktrack_fastapi.core.security import get_password_hash

async def test_rate_limit_within_limit_returns_200(async_client: AsyncClient):
    """Requisições dentro do limite retornam sucesso."""
    response = await async_client.get('/health')
    assert response.status_code == HTTPStatus.OK

async def test_rate_limit_exceeding_returns_429_with_header(async_client: AsyncClient):
    """Ao exceder o limite, retorna 429 e o header Retry-After."""
    # O limite do health_check é 20/minuto
    for _ in range(20):
        await async_client.get('/health')
        
    response = await async_client.get('/health')
    assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
    assert "retry-after" in response.headers

async def test_rate_limit_login_blocked_after_10_attempts(async_client: AsyncClient):
    """Login bloqueado após 10 tentativas pelo mesmo IP."""
    data = {"username": "wrong@test.com", "password": "wrongpassword"}
    
    # Consome as 10 tentativas permitidas
    for _ in range(10):
        response = await async_client.post('/auth/token', data=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        
    # A 11ª tentativa deve ser bloqueada
    response = await async_client.post('/auth/token', data=data)
    assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
    assert "retry-after" in response.headers

async def test_rate_limit_independent_counters_per_user(async_client: AsyncClient, admin_token: str, async_session):
    """Contadores independentes por usuário (usuário A não afeta usuário B)."""
    # Criar um segundo admin
    user2 = User(
        username='admin2_user',
        email='admin2@test.com',
        password=get_password_hash('adminpass'),
        role='admin',
    )
    async_session.add(user2)
    await async_session.commit()
    
    response = await async_client.post(
        '/auth/token',
        data={'username': 'admin2@test.com', 'password': 'adminpass'},
    )
    admin2_token = response.json()['access_token']
    
    headers_user1 = {"Authorization": f"Bearer {admin_token}"}
    headers_user2 = {"Authorization": f"Bearer {admin2_token}"}
    
    # POST em authors tem limite de 30/minuto por usuário
    # Usuário 1 esgota seu limite
    for i in range(30):
        resp = await async_client.post("/authors", json={"name": f"author_{i}"}, headers=headers_user1)
        assert resp.status_code == HTTPStatus.CREATED
        
    # Usuário 1 tenta a 31ª requisição e é bloqueado
    resp_blocked = await async_client.post("/authors", json={"name": "author_blocked"}, headers=headers_user1)
    assert resp_blocked.status_code == HTTPStatus.TOO_MANY_REQUESTS
    
    # Usuário 2 não deve ser afetado
    resp_success = await async_client.post("/authors", json={"name": "author_user2"}, headers=headers_user2)
    assert resp_success.status_code == HTTPStatus.CREATED
