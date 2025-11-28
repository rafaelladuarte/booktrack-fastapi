from http import HTTPStatus

from jwt import decode

from booktrack_fastapi.core.security import SECRET_KEY, get_password_hash
from booktrack_fastapi.models.users import User


def test_auth_token_success(client, session):
    """Testa login bem-sucedido com retorno de access_token e refresh_token."""

    # Cria um usuário de teste
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('testpassword'),
    )
    session.add(user)
    session.commit()

    # Faz login
    response = client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'testpassword'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'bearer'

    # Verifica se os tokens são válidos
    access_payload = decode(data['access_token'], SECRET_KEY, algorithms=['HS256'])
    refresh_payload = decode(data['refresh_token'], SECRET_KEY, algorithms=['HS256'])

    assert access_payload['sub'] == 'test@example.com'
    assert access_payload['type'] == 'access'
    assert refresh_payload['sub'] == 'test@example.com'
    assert refresh_payload['type'] == 'refresh'


def test_auth_token_invalid_credentials(client, session):
    """Testa login com credenciais inválidas."""
    response = client.post(
        '/auth/token',
        data={'username': 'wrong@example.com', 'password': 'wrongpassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_auth_token_wrong_password(client, session):
    """Testa login com senha incorreta."""

    # Cria um usuário de teste
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('correctpassword'),
    )
    session.add(user)
    session.commit()

    # Tenta login com senha errada
    response = client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'wrongpassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_auth_refresh_success(client, session):
    """Testa renovação de token com refresh token válido."""

    # Cria um usuário de teste
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('testpassword'),
    )
    session.add(user)
    session.commit()

    # Faz login para obter tokens
    login_response = client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'testpassword'},
    )
    tokens = login_response.json()
    refresh_token = tokens['refresh_token']

    # Usa o refresh token para obter novos tokens
    response = client.post(
        '/auth/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'bearer'

    # Verifica se os novos tokens são válidos
    new_access_payload = decode(
        data['access_token'], SECRET_KEY, algorithms=['HS256']
    )
    new_refresh_payload = decode(
        data['refresh_token'], SECRET_KEY, algorithms=['HS256']
    )

    assert new_access_payload['sub'] == 'test@example.com'
    assert new_access_payload['type'] == 'access'
    assert new_refresh_payload['sub'] == 'test@example.com'
    assert new_refresh_payload['type'] == 'refresh'


def test_auth_refresh_with_access_token(client, session):
    """Testa que não é possível usar access token na rota de refresh."""

    # Cria um usuário de teste
    user = User(
        username='testuser',
        email='test@example.com',
        password=get_password_hash('testpassword'),
    )
    session.add(user)
    session.commit()

    # Faz login para obter tokens
    login_response = client.post(
        '/auth/token',
        data={'username': 'test@example.com', 'password': 'testpassword'},
    )
    tokens = login_response.json()
    access_token = tokens['access_token']

    # Tenta usar access token na rota de refresh (deve falhar)
    response = client.post(
        '/auth/refresh',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert 'Token inválido: esperado tipo refresh' in response.json()['detail']


def test_auth_refresh_invalid_token(client):
    """Testa renovação com token inválido."""
    response = client.post(
        '/auth/refresh',
        headers={'Authorization': 'Bearer invalid-token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Token inválido ou malformado'}
