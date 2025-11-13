from http import HTTPStatus

from fastapi import APIRouter, Depends

from booktrack_fastapi.schemas.readings import Reading, ReadingList, ReadingQuery

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('/', response_model=ReadingList, status_code=HTTPStatus.OK)
def list_readings(filters: ReadingQuery = Depends()):
    return None


@router.put(
    '/{reading_id}',
    response_model=ReadingList,
    status_code=HTTPStatus.OK,
)
def update_readings(reading_id):
    return None
