from http import HTTPStatus

from fastapi import APIRouter, Depends

from booktrack_fastapi.schemas.readings import (
    ReadingList,
    ReadingQuery,
)

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('_X', response_model=ReadingList, status_code=HTTPStatus.OK)
def list_readings(filters: ReadingQuery = Depends()):
    return None


@router.put(
    '/{reading_id}_X',
    response_model=ReadingList,
    status_code=HTTPStatus.OK,
)
def update_readings(reading_id):
    return None
