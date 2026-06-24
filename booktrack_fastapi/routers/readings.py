from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query, Request
from booktrack_fastapi.core.rate_limit import limiter

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser, SessionDep
from booktrack_fastapi.schemas.readings import (
    ReadingCreate,
    ReadingExpanded,
    ReadingList,
    ReadingQuery,
    ReadingUpdate,
)
from booktrack_fastapi.services.readings_service import ReadingsService

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.post('', response_model=ReadingExpanded, status_code=HTTPStatus.CREATED)
@limiter.limit('30/minute')
async def create_reading(
    request: Request,
    data: ReadingCreate,
    db: SessionDep,
    current_user: AdminUser,
):
    service = ReadingsService(db)
    return await service.create(user_id=current_user.id, data=data)


@router.get('', response_model=ReadingList, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_readings(
    request: Request,
    filter_query: Annotated[ReadingQuery, Query()],
    db: SessionDep,
    current_user: CurrentUser,
):
    service = ReadingsService(db=db)

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = await service.list_all()
    else:
        items = await service.list_by_filter(filter_query)

    return {'data': items}


@router.put(
    '/{book_id}',
    status_code=HTTPStatus.OK,
)
@limiter.limit('30/minute')
async def update_readings(
    request: Request,
    book_id: int,
    data: ReadingUpdate,
    db: SessionDep,
    current_user: AdminUser,
):
    service = ReadingsService(db)
    await service.update_by_book_id(book_id, data)
    return {'detail': 'Reading updated successfully!'}
