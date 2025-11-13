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


@router.get('/', response_model=PropertyList, status_code=HTTPStatus.OK)
def list_properties():
    return None


@router.get(
    '/{type}', response_model=PropertyList, status_code=HTTPStatus.OK
)
def list_properties_by_type(type: str):
    return None


@router.post(
    '/{type}', response_model=PropertyCreate, status_code=HTTPStatus.CREATED
)
def create_property(type: PropertyTypeCreate, property: Property):
    return None
