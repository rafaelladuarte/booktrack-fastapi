from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from booktrack_fastapi.repositories.categories_repo import CategoriesRepository


class CategoriesService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CategoriesRepository(db)

    def create(self, name: str, parent_id: int | None = None, min_length: int = 2):
        name = name.strip()

        if len(name) < min_length:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'The category name must be at least {min_length} characters.',
            )

        existing = self.repo.get_by_name_and_parent(name, parent_id)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Category '{name}' already exists at this level.",
            )
        if parent_id is not None:
            parent = self.repo.get_by_parent_id(parent_id)
            if not parent:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f'Parent_id {parent_id} not found.',
                )

        return self.repo.create(name=name, parent_id=parent_id)

    def list_all(self):
        return self.repo.get_all()

    def get_by_id(self, category_id: int):
        obj = self.repo.get_by_id(category_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Category id {category_id} not found.',
            )
        return obj

    def get_by_parent_id(self, parent_id: int):
        obj = self.repo.get_by_parent_id(parent_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Parent_id {parent_id} not found.',
            )
        return obj

    def list_by_filter(self, **filters):
        return self.repo.get_filtered(**filters)
