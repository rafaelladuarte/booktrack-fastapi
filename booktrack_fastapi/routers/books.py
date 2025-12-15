from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
async def list_book(
    filter_query: Annotated[BookFilter, Query()],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)

    empty = all(v is None for v in filter_query.model_dump().values())
    if empty:
        items = await service.list_all()
    else:
        items = await service.list_by_filter(filter_query)

    return {'data': [expand_book_row(item) for item in items]}


@router.get('/{book_id}', response_model=BookExpandedList, status_code=HTTPStatus.OK)
async def list_book_by_id(
    book_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)

    item = await service.get_by_id(book_id=book_id)
    return {'data': [expand_book_row(item)]}


@router.post('', status_code=HTTPStatus.CREATED)
async def create_book(
    data: BookCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)
    await service.create(data=data)
    return {'detail': 'Book created successfully!'}


@router.put('/{book_id}', status_code=HTTPStatus.OK)
async def update_book(
    book_id: int,
    data: BookUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)
    await service.update_by_id(book_id, data)
    return {'detail': 'Book updated successfully!'}


@router.delete('/{book_id}', status_code=HTTPStatus.OK)
async def delete_book_by_id(
    book_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = BooksService(db)
    await service.delete_by_id(book_id)
    return {'detail': 'Book deleted successfully!'}
