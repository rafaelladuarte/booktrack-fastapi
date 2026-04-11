from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from booktrack_fastapi.core.dependencies import CurrentUser, SessionDep
from booktrack_fastapi.schemas.readings import (
    ReadingList,
    ReadingQuery,
    ReadingUpdate,
)
from booktrack_fastapi.services.readings_service import ReadingsService

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('', response_model=ReadingList, status_code=HTTPStatus.OK)
async def list_readings(
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
async def update_readings(
    book_id: int,
    data: ReadingUpdate,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = ReadingsService(db)
    await service.update_by_book_id(book_id, data)
    return {'detail': 'Reading updated successfully!'}
