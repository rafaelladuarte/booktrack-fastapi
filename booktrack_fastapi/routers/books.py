from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.schemas.books import Book, BookExpandedList, BookFilter
from booktrack_fastapi.services.books_service import BooksService
from booktrack_fastapi.utility.tools import expand_book_row

router = APIRouter(prefix='/books', tags=['Books'])


@router.get('/', response_model=BookExpandedList, status_code=HTTPStatus.OK)
def list_book(
    filter_query: Annotated[BookFilter, Query()], db: Session = Depends(get_session)
):
    service = BooksService(db)

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = service.list_all()
    else:
        items = service.list_by_filter(filter_query)

    return {'data': [expand_book_row(item) for item in items]}


@router.get('/{book_id}', response_model=BookExpandedList, status_code=HTTPStatus.OK)
def list_book_by_id(book_id: int, db: Session = Depends(get_session)):
    service = BooksService(db)

    item = service.get_by_id(book_id=book_id)
    return {'data': [expand_book_row(item)]}


# @router.get('/public', response_model=BookList, status_code=HTTPStatus.OK)
# def list_books_public():
#     return None


@router.post('/', response_model=Book, status_code=HTTPStatus.CREATED)
def create_book():
    return None


@router.put('/{book_id}', response_model=Book, status_code=HTTPStatus.CREATED)
def update_book(book_id: int):
    return None


@router.delete('/{book_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_book_by_id(book_id: int):
    return None
