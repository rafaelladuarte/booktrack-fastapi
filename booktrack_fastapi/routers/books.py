from http import HTTPStatus

from fastapi import APIRouter, Depends

from booktrack_fastapi.schemas.books import Book, BookList, BookQuery

router = APIRouter(prefix='/books', tags=['Books'])


@router.get('/', response_model=BookList, status_code=HTTPStatus.OK)
def list_book(filters: BookQuery = Depends()):
    return None


@router.get('/{book_id}', response_model=BookList, status_code=HTTPStatus.OK)
def list_book_by_id(book_id: int):
    return None


@router.get('/public', response_model=BookList, status_code=HTTPStatus.OK)
def list_books_public():
    return None


@router.post('/', response_model=Book, status_code=HTTPStatus.CREATED)
def create_book():
    return None


@router.put('/{book_id}', response_model=Book, status_code=HTTPStatus.CREATED)
def update_book(book_id: int):
    return None


@router.delete('/{book_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_book_by_id(book_id: int):
    return None
