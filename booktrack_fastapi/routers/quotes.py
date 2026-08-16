from http import HTTPStatus

from fastapi import APIRouter, Request

from booktrack_fastapi.core.dependencies import AdminUser, SessionDep
from booktrack_fastapi.core.rate_limit import limiter
from booktrack_fastapi.schemas.quotes import QuoteCreate, QuoteSchema
from booktrack_fastapi.services.quotes_service import QuotesService

router = APIRouter(prefix='/quotes', tags=['Quotes'])


@router.post('/{reading_id}', response_model=QuoteSchema, status_code=HTTPStatus.CREATED)
@limiter.limit('30/minute')
async def create_quote(
    request: Request,
    reading_id: int,
    data: QuoteCreate,
    db: SessionDep,
    current_user: AdminUser,
):
    """Cria uma nova citação ou nota associada a uma leitura específica."""
    service = QuotesService(db)
    return await service.create(reading_id=reading_id, data=data)


@router.delete('/{quote_id}', status_code=HTTPStatus.NO_CONTENT)
@limiter.limit('30/minute')
async def delete_quote(
    request: Request,
    quote_id: int,
    db: SessionDep,
    current_user: AdminUser,
):
    """Deleta uma citação pelo seu ID."""
    service = QuotesService(db)
    await service.delete(quote_id=quote_id)
