from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from booktrack_fastapi.core.rate_limit import limiter

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser
from booktrack_fastapi.repositories.authors_repo import AuthorsRepository
from booktrack_fastapi.schemas.authors import (
    Author,
    AuthorCreate,
    AuthorList,
    AuthorUpdate,
)

router = APIRouter(prefix='/authors', tags=['Authors'])

AuthorsRepo = Annotated[AuthorsRepository, Depends()]


@router.get('', response_model=AuthorList, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_author(
    request: Request,
    repo: AuthorsRepo,
    current_user: CurrentUser,
):
    items = await repo.get_all()
    return {'data': items}


@router.get('/{author_id}', response_model=AuthorList, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_author_by_id(
    request: Request,
    author_id: int,
    repo: AuthorsRepo,
    current_user: CurrentUser,
):
    item = await repo.get_by_id(author_id)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Author_id {author_id} not found.',
        )
    return {'data': [item]}


@router.post('', response_model=Author, status_code=HTTPStatus.CREATED)
@limiter.limit('30/minute')
async def create_author(
    request: Request,
    data: AuthorCreate,
    repo: AuthorsRepo,
    current_user: AdminUser,
):
    return await repo.create(data.model_dump())


@router.put('/{author_id}', response_model=Author, status_code=HTTPStatus.OK)
@limiter.limit('30/minute')
async def update_author(
    request: Request,
    author_id: int,
    data: AuthorUpdate,
    repo: AuthorsRepo,
    current_user: AdminUser,
):
    item = await repo.get_by_id(author_id)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Author_id {author_id} not found.',
        )
    return await repo.update_by_id(author_id, data.model_dump(exclude_unset=True))


@router.delete('/{author_id}', status_code=HTTPStatus.NO_CONTENT)
@limiter.limit('30/minute')
async def delete_author_by_id(
    request: Request,
    author_id: int,
    repo: AuthorsRepo,
    current_user: AdminUser,
):
    item = await repo.get_by_id(author_id)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Author_id {author_id} not found.',
        )
    await repo.delete_by_id(author_id)
