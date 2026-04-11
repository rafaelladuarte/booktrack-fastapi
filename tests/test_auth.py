from http import HTTPStatus

from httpx import AsyncClient
from jwt import decode
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.core.security import SECRET_KEY, get_password_hash
from booktrack_fastapi.models.users import User


async def test_auth_token_success(async_client: AsyncClient, async_session: AsyncSession):
    """Testa login bem-sucedido com retorno de access_token e refresh_token."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('testpassword'),
    )
    async_session.add(user)
    await async_session.commit()

    # O campo 'username' do formulário OAuth2 recebe o e-mail do usuário.
    # Isso é uma limitação do protocolo OAuth2PasswordRequestForm — ver BT-002.
    response = await async_client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'testpassword'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'bearer'

    access_payload = decode(data['access_token'], SECRET_KEY, algorithms=['HS256'])
    refresh_payload = decode(data['refresh_token'], SECRET_KEY, algorithms=['HS256'])

    assert access_payload['sub'] == 'test@example.com'
    assert access_payload['type'] == 'access'
    assert refresh_payload['sub'] == 'test@example.com'
    assert refresh_payload['type'] == 'refresh'


async def test_auth_token_invalid_credentials(async_client: AsyncClient):
    """Testa login com credenciais inválidas."""
    response = await async_client.post(
        '/auth/token',
        data={'username': 'wrong@example.com', 'password': 'wrongpassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


async def test_auth_token_wrong_password(
    async_client: AsyncClient, async_session: AsyncSession
):
    """Testa login com senha incorreta."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('correctpassword'),
    )
    async_session.add(user)
    await async_session.commit()

    response = await async_client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'wrongpassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


async def test_auth_refresh_success(
    async_client: AsyncClient, async_session: AsyncSession
):
    """Testa renovação de token com refresh token válido."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('testpassword'),
    )
    async_session.add(user)
    await async_session.commit()

    login_response = await async_client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'testpassword'},
    )
    tokens = login_response.json()
    refresh_token = tokens['refresh_token']

    response = await async_client.post(
        '/auth/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'bearer'

    new_access_payload = decode(data['access_token'], SECRET_KEY, algorithms=['HS256'])
    new_refresh_payload = decode(data['refresh_token'], SECRET_KEY, algorithms=['HS256'])

    assert new_access_payload['sub'] == 'test@example.com'
    assert new_access_payload['type'] == 'access'
    assert new_refresh_payload['sub'] == 'test@example.com'
    assert new_refresh_payload['type'] == 'refresh'


async def test_auth_refresh_with_access_token(
    async_client: AsyncClient, async_session: AsyncSession
):
    """Testa que não é possível usar access token na rota de refresh."""
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('testpassword'),
    )
    async_session.add(user)
    await async_session.commit()

    login_response = await async_client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'testpassword'},
    )
    tokens = login_response.json()
    access_token = tokens['access_token']

    response = await async_client.post(
        '/auth/refresh',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert 'Token inválido: esperado tipo refresh' in response.json()['detail']


async def test_auth_refresh_invalid_token(async_client: AsyncClient):
    """Testa renovação com token inválido."""
    response = await async_client.post(
        '/auth/refresh',
        headers={'Authorization': 'Bearer invalid-token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Token inválido ou malformado'}
