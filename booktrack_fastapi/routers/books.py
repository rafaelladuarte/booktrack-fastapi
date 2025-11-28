from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import get_current_user
from booktrack_fastapi.models.users import User
from booktrack_fastapi.schemas.books import (
    BookCreate,
    BookExpandedList,
    BookFilter,
    BookUpdate,
)
from booktrack_fastapi.services.books_service import BooksService
from booktrack_fastapi.utility.tools import expand_book_row

router = APIRouter(prefix='/books', tags=['Books'])


@router.get('', response_model=BookExpandedList, status_code=HTTPStatus.OK)
def list_book(
    filter_query: Annotated[BookFilter, Query()],
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = service.list_all()
    else:
        items = service.list_by_filter(filter_query)

    return {'data': [expand_book_row(item) for item in items]}


@router.get('/{book_id}', response_model=BookExpandedList, status_code=HTTPStatus.OK)
def list_book_by_id(
    book_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)

    item = service.get_by_id(book_id=book_id)
    return {'data': [expand_book_row(item)]}


@router.post('', status_code=HTTPStatus.CREATED)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)
    service.create(data=data)
    return {'detail': 'Book created successfully!'}


@router.put('/{book_id}', status_code=HTTPStatus.OK)
def update_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)
    service.update_by_id(book_id, data)
    return {'detail': 'Book updated successfully!'}


@router.delete('/{book_id}', status_code=HTTPStatus.OK)
def delete_book_by_id(
    book_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)
    service.delete_by_id(book_id)
    return {'detail': 'Book deleted successfully!'}
