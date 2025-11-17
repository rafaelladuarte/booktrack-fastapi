from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.tags import Tags
from booktrack_fastapi.models.shelves import Shelves
from booktrack_fastapi.repositories.properties_repo import PropertiesRepository
from booktrack_fastapi.schemas.properties import PropertyList, PropertyType, PropertyCreate, PropertyTypeCreate, Property
from booktrack_fastapi.services.properties_service import PropertiesService

router = APIRouter(prefix='/properties', tags=['Properties'])

PROPERTY_MODEL_MAP = {
    PropertyType.publishers: Publishers,
    PropertyType.collections: Collections,
    PropertyType.formats: Formats,
    PropertyType.formats: ReadingStatus,
    PropertyType.formats: Tags,
    PropertyType.formats: Shelves
}


@router.get('/{type}', response_model=PropertyList, status_code=HTTPStatus.OK)
def list_properties_by_type(
    type: PropertyType, db: Session = Depends(get_session)
):
    model = PROPERTY_MODEL_MAP[type]

    service = PropertiesService(
        db=db, model=model, repository_cls=PropertiesRepository
    )

    items = service.list_all()
    return {"data": items}


@router.post(
    '/{type}', response_model=PropertyCreate, status_code=HTTPStatus.CREATED
)
def create_property(
    type: PropertyTypeCreate,
    property: Property,
    db: Session = Depends(get_session)
):
    model = PROPERTY_MODEL_MAP[type]

    service = PropertiesService(
        db=db, model=model, repository_cls=PropertiesRepository
    )

    items = service.create(name=property.name)
    
    return {"data": items}