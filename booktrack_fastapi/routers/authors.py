from http import HTTPStatus

from fastapi import APIRouter

from booktrack_fastapi.core.dependencies import CurrentUser, SessionDep
from booktrack_fastapi.schemas.authors import (
    Author,
    AuthorCreate,
    AuthorList,
    AuthorUpdate,
)
from booktrack_fastapi.services.authors_service import AuthorsService

router = APIRouter(prefix='/authors', tags=['Authors'])


@router.get('', response_model=AuthorList, status_code=HTTPStatus.OK)
async def list_author(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = AuthorsService(db)
    items = await service.list_all()
    return {'data': items}


@router.get('/{author_id}', response_model=AuthorList, status_code=HTTPStatus.OK)
async def list_author_by_id(
    author_id: int,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = AuthorsService(db)
    item = await service.get_by_id(author_id)
    return {'data': [item]}


@router.post('', response_model=Author, status_code=HTTPStatus.CREATED)
async def create_author(
    data: AuthorCreate,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = AuthorsService(db)
    return await service.create(data)


@router.put('/{author_id}', response_model=Author, status_code=HTTPStatus.OK)
async def update_author(
    author_id: int,
    data: AuthorUpdate,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = AuthorsService(db)
    return await service.update(author_id, data)


@router.delete('/{author_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_author_by_id(
    author_id: int,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = AuthorsService(db)
    await service.delete(author_id)
