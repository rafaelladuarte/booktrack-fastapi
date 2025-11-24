from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.repositories.readings_repo import ReadingsRepository
from booktrack_fastapi.services.readings_service import ReadingsService
from booktrack_fastapi.schemas.readings import (
    ReadingList,
    ReadingQuery,
    ReadingUpdate,
)

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('', response_model=ReadingList, status_code=HTTPStatus.OK)
def list_readings(filter_query: Annotated[ReadingQuery, Query()], db: Session = Depends(get_session)):
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
def update_readings(book_id: int, data: ReadingUpdate, db: Session = Depends(get_session)):
    service = ReadingsService(db)
    service.update_by_book_id(book_id, data)
    return {'detail': 'Reading updated successfully!'}
