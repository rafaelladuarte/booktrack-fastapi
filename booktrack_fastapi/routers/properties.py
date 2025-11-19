from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.shelves import Shelves
from booktrack_fastapi.models.tags import Tags
from booktrack_fastapi.repositories.properties_repo import PropertiesRepository
from booktrack_fastapi.schemas.properties import (
    # Property,
    PropertyCreate,
    PropertyList,
    PropertyType,
    PropertyTypeCreate,
)
from booktrack_fastapi.services.properties_service import PropertiesService

router = APIRouter(prefix='/properties', tags=['Properties'])

PROPERTY_MODEL_MAP = {
    PropertyType.publishers: Publishers,
    PropertyType.collections: Collections,
    PropertyType.formats: Formats,
    PropertyType.reading_status: ReadingStatus,
    PropertyType.tags: Tags,
    PropertyType.shelves: Shelves,
}


@router.get('/{type}', response_model=PropertyList, status_code=HTTPStatus.OK)
def list_properties_by_type(type: PropertyType, db: Session = Depends(get_session)):
    model = PROPERTY_MODEL_MAP[type]

    service = PropertiesService(
        db=db, model=model, repository_cls=PropertiesRepository
    )

    items = service.list_all()

    return {'data': items}


@router.post(
    '/{type}', response_model=PropertyCreate, status_code=HTTPStatus.CREATED
)
def create_property(
    type: PropertyTypeCreate, name: str, db: Session = Depends(get_session)
):
    model = PROPERTY_MODEL_MAP[type]

    if not model:
        raise HTTPException(400, 'Tipo inválido')

    service = PropertiesService(
        db=db, model=model, repository_cls=PropertiesRepository
    )

    item = service.create(name=name)

    return {'data': item.name}
