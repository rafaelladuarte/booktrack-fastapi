from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query, Request
from booktrack_fastapi.core.rate_limit import limiter

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser, SessionDep
from booktrack_fastapi.schemas.books import (
    BookCreate,
    BookExpandedList,
    BookDetailList,
    BookFilter,
    BookUpdate,
)
from booktrack_fastapi.services.books_service import BooksService

router = APIRouter(prefix='/books', tags=['Books'])


@router.get('', response_model=BookExpandedList, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_book(
    request: Request,
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


@router.get('/{book_id}', response_model=BookDetailList, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_book_by_id(
    request: Request,
    book_id: int,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = BooksService(db)

    item = await service.get_by_id(book_id=book_id)
    return {'data': [item]}


@router.post('', status_code=HTTPStatus.CREATED)
@limiter.limit('30/minute')
async def create_book(
    request: Request,
    data: BookCreate,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = BooksService(db)
    await service.create(data=data)
    return {'detail': 'Book created successfully!'}


@router.put('/{book_id}', status_code=HTTPStatus.OK)
@limiter.limit('30/minute')
async def update_book(
    request: Request,
    book_id: int,
    data: BookUpdate,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = BooksService(db)
    await service.update_by_id(book_id, data)
    return {'detail': 'Book updated successfully!'}


@router.delete('/{book_id}', status_code=HTTPStatus.OK)
@limiter.limit('30/minute')
async def delete_book_by_id(
    request: Request,
    book_id: int,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = BooksService(db)
    await service.delete_by_id(book_id)
    return {'detail': 'Book deleted successfully!'}
