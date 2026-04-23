from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser, SessionDep
from booktrack_fastapi.schemas.books import (
    BookCreate,
    BookExpandedList,
    BookFilter,
    BookUpdate,
)
from booktrack_fastapi.services.books_service import BooksService

router = APIRouter(prefix='/books', tags=['Books'])


@router.get('', response_model=BookExpandedList, status_code=HTTPStatus.OK)
async def list_book(
    filter_query: Annotated[BookFilter, Query()],
    db: SessionDep,
    current_user: CurrentUser,
):
    service = BooksService(db)

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = await service.list_all()
    else:
        items = await service.list_by_filter(filter_query)

    return {'data': items}


@router.get('/{book_id}', response_model=BookExpandedList, status_code=HTTPStatus.OK)
async def list_book_by_id(
    book_id: int,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = BooksService(db)

    item = await service.get_by_id(book_id=book_id)
    return {'data': [item]}


@router.post('', status_code=HTTPStatus.CREATED)
async def create_book(
    data: BookCreate,
    db: SessionDep,
    current_user: AdminUser,
):
    service = BooksService(db)
    await service.create(data=data)
    return {'detail': 'Book created successfully!'}


@router.put('/{book_id}', status_code=HTTPStatus.OK)
async def update_book(
    book_id: int,
    data: BookUpdate,
    db: SessionDep,
    current_user: AdminUser,
):
    service = BooksService(db)
    await service.update_by_id(book_id, data)
    return {'detail': 'Book updated successfully!'}


@router.delete('/{book_id}', status_code=HTTPStatus.OK)
async def delete_book_by_id(
    book_id: int,
    db: SessionDep,
    current_user: AdminUser,
):
    service = BooksService(db)
    await service.delete_by_id(book_id)
    return {'detail': 'Book deleted successfully!'}
