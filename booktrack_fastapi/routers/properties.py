from http import HTTPStatus

from fastapi import APIRouter

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser, SessionDep
from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.shelves import Shelves
from booktrack_fastapi.models.tags import Tags
from booktrack_fastapi.repositories.properties_repo import PropertiesRepository
from booktrack_fastapi.schemas.properties import (
    PropertyCreate,
    PropertyList,
)
from booktrack_fastapi.services.properties_service import PropertiesService

router = APIRouter(tags=['Properties'])


@router.get('/collections', response_model=PropertyList, status_code=HTTPStatus.OK)
async def list_collections(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = PropertiesService(db=db, model=Collections, repository_cls=PropertiesRepository)
    items = await service.list_all()
    return {'data': items}


@router.post('/collections', response_model=PropertyCreate, status_code=HTTPStatus.CREATED)
async def create_collection(
    name: str,
    db: SessionDep,
    current_user: AdminUser,
):
    service = PropertiesService(db=db, model=Collections, repository_cls=PropertiesRepository)
    await service.create(name=name)
    return {'detail': 'Collection created successfully!'}


@router.get('/publishers', response_model=PropertyList, status_code=HTTPStatus.OK)
async def list_publisher(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = PropertiesService(db=db, model=Publishers, repository_cls=PropertiesRepository)
    items = await service.list_all()
    return {'data': items}


@router.post('/publishers', status_code=HTTPStatus.CREATED)
async def create_publisher(
    name: str,
    db: SessionDep,
    current_user: AdminUser,
):
    service = PropertiesService(db=db, model=Publishers, repository_cls=PropertiesRepository)
    await service.create(name=name)
    return {'detail': 'Publisher created successfully!'}


@router.get('/tags', response_model=PropertyList, status_code=HTTPStatus.OK)
async def list_tags(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = PropertiesService(db=db, model=Tags, repository_cls=PropertiesRepository)
    items = await service.list_all()
    return {'data': items}


@router.post('/tags', status_code=HTTPStatus.CREATED)
async def create_tags(
    name: str,
    db: SessionDep,
    current_user: AdminUser,
):
    service = PropertiesService(db=db, model=Tags, repository_cls=PropertiesRepository)
    await service.create(name=name)
    return {'detail': 'Tag created successfully!'}


@router.get('/shelves', response_model=PropertyList, status_code=HTTPStatus.OK)
async def list_shelves(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = PropertiesService(db=db, model=Shelves, repository_cls=PropertiesRepository)
    items = await service.list_all()
    return {'data': items}


@router.get('/reading_status', response_model=PropertyList, status_code=HTTPStatus.OK)
async def list_reading_status(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = PropertiesService(db=db, model=ReadingStatus, repository_cls=PropertiesRepository)
    items = await service.list_all()
    return {'data': items}


@router.get('/formats', response_model=PropertyList, status_code=HTTPStatus.OK)
async def list_formats(
    db: SessionDep,
    current_user: CurrentUser,
):
    service = PropertiesService(db=db, model=Formats, repository_cls=PropertiesRepository)
    items = await service.list_all()
    return {'data': items}
