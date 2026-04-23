from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import get_password_hash
from booktrack_fastapi.main import app
from booktrack_fastapi.models.base import Base
from booktrack_fastapi.models.users import User, table_registry

# ---------------------------------------------------------------------------
# Fixtures SÍNCRONAS — usadas por test_properties.py (sem rotas async)
# ---------------------------------------------------------------------------


@pytest.fixture
def session():
    """Sessão síncrona SQLite in-memory para testes de modelo direto."""
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    table_registry.metadata.drop_all(engine)
    engine.dispose()


# ---------------------------------------------------------------------------
# Fixtures ASSÍNCRONAS — usadas por test_auth.py e test_readings.py
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def async_session():
    """AsyncSession SQLite in-memory para testes assíncronos."""
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(table_registry.metadata.create_all)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(table_registry.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def async_client(async_session):
    """AsyncClient com sessão async para testes de rotas assíncronas."""

    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def client(async_session):
    """TestClient síncrono com sessão async — compatível com endpoints async."""

    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_token(async_session, async_client):
    """Cria um usuário admin e retorna apenas o token de acesso."""
    user = User(
        username='admin_user',
        email='admin@test.com',
        password=get_password_hash('adminpass'),
        role='admin',
    )
    async_session.add(user)
    await async_session.commit()

    response = await async_client.post(
        '/auth/token',
        data={'username': 'admin@test.com', 'password': 'adminpass'},
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def admin_headers(admin_token):
    """Retorna headers com o token de admin válido."""
    return {'Authorization': f'Bearer {admin_token}'}


@pytest_asyncio.fixture
async def viewer_token(async_session, async_client):
    """Cria um usuário viewer e retorna apenas o token de acesso."""
    user = User(
        username='viewer_user',
        email='viewer@test.com',
        password=get_password_hash('viewerpass'),
        role='viewer',
    )
    async_session.add(user)
    await async_session.commit()

    response = await async_client.post(
        '/auth/token',
        data={'username': 'viewer@test.com', 'password': 'viewerpass'},
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def viewer_headers(viewer_token):
    """Retorna headers com o token de viewer válido."""
    return {'Authorization': f'Bearer {viewer_token}'}


# ---------------------------------------------------------------------------
# Utilitário — mock de timestamps
# ---------------------------------------------------------------------------


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)
    yield time
    event.remove(model, 'before_insert', fake_time_handler)


@pytest_asyncio.fixture
async def auth_headers(viewer_headers):
    """Alias para viewer_headers para manter compatibilidade."""
    return viewer_headers


@pytest.fixture
def mock_db_time():
    return _mock_db_time
