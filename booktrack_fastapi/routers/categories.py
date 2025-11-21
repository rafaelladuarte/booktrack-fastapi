from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.schemas.categories import (
    CategoriesList,
    Category,
    CategoryCreate,
    CategoryParentFilter,
)
from booktrack_fastapi.services.categories_service import CategoriesService

router = APIRouter(prefix='/categories', tags=['Categories'])


@router.get('', response_model=CategoriesList, status_code=HTTPStatus.OK)
def list_categories(
    filter_query: Annotated[CategoryParentFilter, Query()],
    db: Session = Depends(get_session),
):
    service = CategoriesService(db)

    parent_id = filter_query.parent_id
    if parent_id:
        items = service.get_by_parent_id(parent_id)

        result_item = []
        for item in items:
            result_item.append({
                'id': item.id,
                'name': item.name,
                'parent_id': item.parent_id,
            })

        return {'data': result_item}

    items = service.list_all()

    result_item = []
    for item in items:
        result_item.append({
            'id': item.id,
            'name': item.name,
            'parent_id': item.parent_id,
        })

    return {'data': result_item}


@router.get('/{category_id}', response_model=Category, status_code=HTTPStatus.OK)
def list_categories_by_id(category_id: int, db: Session = Depends(get_session)):
    service = CategoriesService(db)

    item = service.get_by_id(category_id)
    return {'id': item.id, 'name': item.name, 'parent_id': item.parent_id}


@router.post('', response_model=Category, status_code=HTTPStatus.CREATED)
def create_categorie(data: CategoryCreate, db: Session = Depends(get_session)):
    service = CategoriesService(db)
    item = service.create(name=data.name, parent_id=data.parent_id)

    return {'id': item.id, 'name': item.name, 'parent_id': item.parent_id}
