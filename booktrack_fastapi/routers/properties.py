from http import HTTPStatus

from fastapi import APIRouter

from booktrack_fastapi.schemas.properties import (
    Property,
    PropertyCreate,
    PropertyList,
    PropertyType,
    PropertyTypeCreate,
)

router = APIRouter(prefix='/properties', tags=['Properties'])


@router.get('/', response_model=PropertyType, status_code=HTTPStatus.OK)
def list_properties():
    return PropertyType


@router.get(
    '/{type}', response_model=PropertyList, status_code=HTTPStatus.OK
)
def list_properties_by_type(type: str):
    return {'id': 1, 'name': type}


@router.post(
    '/{type}', response_model=PropertyCreate, status_code=HTTPStatus.CREATED
)
def create_property(type: PropertyTypeCreate, property: Property):
    return {'name': property.name}
