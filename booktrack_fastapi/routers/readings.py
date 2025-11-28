from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import get_current_user
from booktrack_fastapi.models.users import User
from booktrack_fastapi.schemas.readings import (
    ReadingList,
    ReadingQuery,
    ReadingUpdate,
)
from booktrack_fastapi.services.readings_service import ReadingsService

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('', response_model=ReadingList, status_code=HTTPStatus.OK)
def list_readings(
    filter_query: Annotated[ReadingQuery, Query()],
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ReadingsService(
        db=db
    )

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = service.list_all()
    else:
        items = service.list_by_filter(filter_query)

    return {'data': items}


@router.put(
    '/{book_id}',
    status_code=HTTPStatus.OK,
)
def update_readings(
    book_id: int,
    data: ReadingUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = ReadingsService(db)
    service.update_by_book_id(book_id, data)
    return {'detail': 'Reading updated successfully!'}
