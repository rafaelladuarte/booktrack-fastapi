from http import HTTPStatus

from fastapi import APIRouter

from booktrack_fastapi.schemas.readings import Reading, ReadingList

router = APIRouter(prefix='/readings', tags=['Readings'])


@router.get('/', response_model=list[Reading], status_code=HTTPStatus.OK)
def list_readings():
    return None


@router.put(
    '/{reading_id}',
    response_model=list[ReadingList],
    status_code=HTTPStatus.OK,
)
def update_readings(reading_id):
    return None
