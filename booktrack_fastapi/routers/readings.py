from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import get_current_user
from booktrack_fastapi.models.users import User
from booktrack_fastapi.schemas.readings import (
    ReadingList,
    ReadingQuery,
    ReadingUpdate,
)
from booktrack_fastapi.services.readings_service import ReadingsService
from booktrack_fastapi.utility.tools import expand_reading_row

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('', response_model=ReadingList, status_code=HTTPStatus.OK)
async def list_readings(
    filter_query: Annotated[ReadingQuery, Query()],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ReadingsService(db=db)

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = await service.list_all()
    else:
        items = await service.list_by_filter(filter_query)

    return {'data': [expand_reading_row(item) for item in items]}


@router.put(
    '/{book_id}',
    status_code=HTTPStatus.OK,
)
async def update_readings(
    book_id: int,
    data: ReadingUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ReadingsService(db)
    await service.update_by_book_id(book_id, data)
    return {'detail': 'Reading updated successfully!'}
