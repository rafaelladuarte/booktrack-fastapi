from http import HTTPStatus

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from booktrack_fastapi.core.dependencies import SessionDep


class HealthStatus(BaseModel):
    status: str
    service: str
    version: str


class ReadinessStatus(BaseModel):
    status: str
    database: str


router = APIRouter(tags=['health'])


@router.get('/health', response_model=HealthStatus, status_code=HTTPStatus.OK)
async def health_check():
    """Liveness check para verificar se a aplicação está rodando."""
    return HealthStatus(status='ok', service='booktrack-api', version='0.1.0')


@router.get('/health/ready', response_model=ReadinessStatus)
async def readiness_check(db: SessionDep):
    """Readiness check para verificar conectividade com o banco de dados."""
    try:
        await db.execute(text('SELECT 1'))
        return ReadinessStatus(status='ok', database='connected')
    except Exception:
        return ReadinessStatus(status='unavailable', database='disconnected')
