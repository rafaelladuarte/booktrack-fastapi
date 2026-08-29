from http import HTTPStatus

from fastapi import APIRouter, Request

from booktrack_fastapi.core.dependencies import AdminUser, SessionDep
from booktrack_fastapi.core.rate_limit import limiter
from booktrack_fastapi.schemas.quotes import QuoteCreate, QuoteSchema, QuoteList
from booktrack_fastapi.services.quotes_service import QuotesService
from fastapi import Query

router = APIRouter(prefix='/quotes', tags=['Quotes'])


@router.get('/{reading_id}', response_model=QuoteList, status_code=HTTPStatus.OK)
@limiter.limit('60/minute')
async def list_quotes(
    request: Request,
    reading_id: int,
    db: SessionDep,
    current_user: AdminUser,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Lista citações de uma leitura de forma paginada."""
    service = QuotesService(db)
    quotes = await service.list_by_reading(reading_id=reading_id, limit=limit, offset=offset)
    return {'data': quotes}


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
