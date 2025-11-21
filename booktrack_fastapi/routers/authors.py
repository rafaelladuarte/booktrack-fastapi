from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session

router = APIRouter(prefix='/authors', tags=['Authors'])


@router.get('_X', status_code=HTTPStatus.OK)
def list_author(db: Session = Depends(get_session)):
    return None


@router.get('/{author_id}_X', status_code=HTTPStatus.OK)
def list_author_by_id(author_id: int, db: Session = Depends(get_session)):
    return None


@router.post('_X', status_code=HTTPStatus.CREATED)
def create_author(db: Session = Depends(get_session)):
    return {'detail': 'Author created successfully!'}


@router.put('/{author_id}_X', status_code=HTTPStatus.CREATED)
def update_author(author_id: int):
    return None


@router.delete('/{author_id}_X', status_code=HTTPStatus.NO_CONTENT)
def delete_author_by_id(author_id: int):
    return None
