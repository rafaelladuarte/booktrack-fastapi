from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from booktrack_fastapi.core.dependencies import CurrentUser
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
async def list_author(
    repo: AuthorsRepo,
    current_user: CurrentUser,
):
    items = await repo.get_all()
    return {'data': items}


@router.get('/{author_id}', response_model=AuthorList, status_code=HTTPStatus.OK)
async def list_author_by_id(
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
async def create_author(
    data: AuthorCreate,
    repo: AuthorsRepo,
    current_user: CurrentUser,
):
    return await repo.create(data.model_dump())


@router.put('/{author_id}', response_model=Author, status_code=HTTPStatus.OK)
async def update_author(
    author_id: int,
    data: AuthorUpdate,
    repo: AuthorsRepo,
    current_user: CurrentUser,
):
    item = await repo.get_by_id(author_id)
    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Author_id {author_id} not found.',
        )
    return await repo.update_by_id(author_id, data.model_dump(exclude_unset=True))


@router.delete('/{author_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_author_by_id(
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
    await repo.delete_by_id(author_id)
