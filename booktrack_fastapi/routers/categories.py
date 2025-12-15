from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import get_current_user
from booktrack_fastapi.models.users import User
from booktrack_fastapi.schemas.categories import (
    CategoriesList,
    Category,
    CategoryCreate,
    CategoryParentFilter,
)
from booktrack_fastapi.services.categories_service import CategoriesService

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.get('', response_model=CategoriesList, status_code=HTTPStatus.OK)
async def list_categories(
    filter_query: Annotated[CategoryParentFilter, Query()],
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = CategoriesService(db)

    parent_id = filter_query.parent_id
    if parent_id:
        items = await service.get_by_parent_id(parent_id)

        result_item = []
        for item in items:
            result_item.append({
                'id': item.id,
                'name': item.name,
                'parent_id': item.parent_id,
            })

        return {'data': result_item}

    items = await service.list_all()

    result_item = []
    for item in items:
        result_item.append({
            'id': item.id,
            'name': item.name,
            'parent_id': item.parent_id,
        })

    return {'data': result_item}


@router.get('/{category_id}', response_model=Category, status_code=HTTPStatus.OK)
async def list_categories_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = CategoriesService(db)

    item = await service.get_by_id(category_id)
    return {'id': item.id, 'name': item.name, 'parent_id': item.parent_id}


@router.post('', response_model=Category, status_code=HTTPStatus.CREATED)
async def create_categorie(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = CategoriesService(db)
    item = await service.create(name=data.name, parent_id=data.parent_id)

    return {'id': item.id, 'name': item.name, 'parent_id': item.parent_id}
