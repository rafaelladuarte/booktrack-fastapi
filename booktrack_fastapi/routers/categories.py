from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query, Request
from booktrack_fastapi.core.rate_limit import limiter

from booktrack_fastapi.core.dependencies import AdminUser, CurrentUser, SessionDep
from booktrack_fastapi.schemas.categories import (
    CategoriesList,
    Category,
    CategoryCreate,
    CategoryParentFilter,
    CategoryUpdate,
)
from booktrack_fastapi.services.categories_service import CategoriesService

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.get('', response_model=CategoriesList, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_categories(
    request: Request,
    filter_query: Annotated[CategoryParentFilter, Query()],
    db: SessionDep,
    current_user: CurrentUser,
):
    """Lista categorias vinculadas ou sem filtros aplicados.

    Args:
        filter_query: Parâmetros Query para filtrar listagem (ex: parent_id).
        db: Sessão de banco de dados assíncrona injetada.
        current_user: Usuário autenticado obtido do token.

    Returns:
        Um JSON contendo as categorias agrupadas nas regras de negócio.
    """
    service = CategoriesService(db)
    items = await service.list_by_filter(**filter_query.model_dump(exclude_unset=True))
    return {'data': items}


@router.get('/{category_id}', response_model=Category, status_code=HTTPStatus.OK)
@limiter.limit('100/minute')
async def list_categories_by_id(
    request: Request,
    category_id: int,
    db: SessionDep,
    current_user: CurrentUser,
):
    service = CategoriesService(db)
    return await service.get_by_id(category_id)


@router.post('', response_model=Category, status_code=HTTPStatus.CREATED)
@limiter.limit('30/minute')
async def create_categorie(
    request: Request,
    data: CategoryCreate,
    db: SessionDep,
    current_user: AdminUser,
):
    service = CategoriesService(db)
    return await service.create(name=data.name, parent_id=data.parent_id)

@router.put('/{category_id}', response_model=Category, status_code=HTTPStatus.OK)
@limiter.limit('30/minute')
async def update_categorie(
    request: Request,
    category_id: int,
    data: CategoryUpdate,
    db: SessionDep,
    current_user: AdminUser,
):
    service = CategoriesService(db)
    return await service.update(category_id, data.model_dump(exclude_unset=True))

@router.delete('/{category_id}', status_code=HTTPStatus.OK)
@limiter.limit('30/minute')
async def delete_categorie(
    request: Request,
    category_id: int,
    db: SessionDep,
    current_user: AdminUser,
):
    service = CategoriesService(db)
    await service.delete(category_id)
    return {'detail': 'Category deleted successfully.'}
