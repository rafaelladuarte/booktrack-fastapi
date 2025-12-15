from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from booktrack_fastapi.core.settings import Settings

# Adapta a URL para driver async se for sqlite padrão
database_url = Settings().DATABASE_URL
if database_url.startswith("sqlite://") and "aiosqlite" not in database_url:
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")

# Configurações específicas para SQLite async
connect_args = {}
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(database_url, connect_args=connect_args, echo=False)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
