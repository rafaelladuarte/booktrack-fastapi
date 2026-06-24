from http import HTTPStatus

import pytest
from fastapi import APIRouter

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser
from booktrack_fastapi.main import app

# Router temporário para testar as dependências
test_router = APIRouter(prefix='/test-rbac', tags=['Test RBAC'])


@test_router.get('/admin-only')
async def admin_only_route(user: AdminUser):
    return {'message': f'Hello admin {user.username}'}


@test_router.get('/any-user')
async def any_user_route(user: CurrentUser):
    return {'message': f'Hello user {user.username}'}


# Adicionar o router ao app para o teste
app.include_router(test_router)


@pytest.mark.asyncio
async def test_admin_access_admin_route(async_client, admin_headers):
    response = await async_client.get('/test-rbac/admin-only', headers=admin_headers)
    assert response.status_code == HTTPStatus.OK
    assert 'Hello admin' in response.json()['message']


@pytest.mark.asyncio
async def test_viewer_access_admin_route(async_client, viewer_headers):
    response = await async_client.get('/test-rbac/admin-only', headers=viewer_headers)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert 'Acesso negado' in response.json()['detail']


@pytest.mark.asyncio
async def test_unauthenticated_access_admin_route(async_client):
    response = await async_client.get('/test-rbac/admin-only')
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_admin_access_any_route(async_client, admin_headers):
    response = await async_client.get('/test-rbac/any-user', headers=admin_headers)
    assert response.status_code == HTTPStatus.OK
    assert 'Hello user' in response.json()['message']


@pytest.mark.asyncio
async def test_viewer_access_any_route(async_client, viewer_headers):
    response = await async_client.get('/test-rbac/any-user', headers=viewer_headers)
    assert response.status_code == HTTPStatus.OK
    assert 'Hello user' in response.json()['message']


@pytest.mark.asyncio
async def test_unauthenticated_access_any_route(async_client):
    response = await async_client.get('/test-rbac/any-user')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
