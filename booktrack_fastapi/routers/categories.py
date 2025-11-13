from http import HTTPStatus

from fastapi import APIRouter

from booktrack_fastapi.schemas.categories import (
    CategoriesList,
    Category,
    CategoryCreate,
)

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.get('/', response_model=CategoriesList, status_code=HTTPStatus.OK)
def list_categories():
    return None


@router.get(
    '/{category_id}', response_model=Category, status_code=HTTPStatus.OK
)
def list_categories_by_id(category_id: int):
    return None


@router.post(
    '/{parent_id}', response_model=Category, status_code=HTTPStatus.CREATED
)
def create_categorie(data: CategoryCreate, parent_id: int):
    return None
