from http import HTTPStatus

from fastapi import APIRouter

from booktrack_fastapi.schemas.properties import Property, PropertyType

router = APIRouter(prefix='/properties', tags=['properties'])


@router.get(
    '/{type}', response_model=list[Property], status_code=HTTPStatus.OK
)
def list_properties(type: PropertyType):
    if type == PropertyType.editoras:
        return [{'id': 1, 'nome': 'Editora'}]
    elif type == PropertyType.formatos:
        return [{'id': 1, 'nome': 'Formato'}]
    elif type == PropertyType.status_leitura:
        return [{'id': 1, 'nome': 'Status Leitura'}]
    elif type == PropertyType.etiquetas:
        return [{'id': 1, 'nome': 'Etiquetas'}]
    elif type == PropertyType.colecoes:
        return [{'id': 1, 'nome': 'Coleções'}]
    elif type == PropertyType.estantes:
        return [{'id': 1, 'nome': 'Estantes'}]


@router.post('/{type}', response_model=Property)
def create_properties(
    type: PropertyType, properties: Property, status_code=HTTPStatus.CREATED
):
    return [{'id': 1, 'nome': properties.name}]
