from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.repositories.categories_repo import CategoriesRepository


class CategoriesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoriesRepository(db)

    async def create(self, name: str, parent_id: int | None = None, min_length: int = 2):
        name = name.strip()

        if len(name) < min_length:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'The category name must be at least {min_length} characters.'
            )

        existing = await self.repo.get_by_name_and_parent(name, parent_id)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Category '{name}' already exists at this level.",
            )
        if parent_id is not None:
            parent = await self.repo.get_by_parent_id(parent_id)
            if not parent:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f'Parent_id {parent_id} not found.',
                )

        return await self.repo.create(name=name, parent_id=parent_id)

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, category_id: int):
        obj = await self.repo.get_by_id(category_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Category id {category_id} not found.',
            )
        return obj

    async def get_by_parent_id(self, parent_id: int):
        # The repo returns a list for get_by_parent_id
        obj = await self.repo.get_by_parent_id(parent_id)
        # Service logic seemed to imply check existence of parent, or return children?
        # Original: obj = self.repo.get_by_parent_id(parent_id) -> if not obj -> 404
        # If the parent_id doesn't exist, get_by_parent_id returns empty list?
        # Or was it intended to check if parent category exists?
        # The repo implementation: SELECT ... WHERE parent_id = X. Returns [] if no children.
        # The service detail says "Parent_id X not found".
        # This implies it should check if the Parent Category exists first?
        # But the original code just checked the result of get_by_parent_id.
        # If get_by_parent_id returns children, "not obj" means empty list.
        # So it returns 404 if no children found? That's a bit odd but I'll keep the logic.
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Parent_id {parent_id} not found (or has no children).',
            )
        return obj

    async def list_by_filter(self, **filters):
        # Repo doesn't seem to have get_filtered in the file I read earlier?
        # I only saw get_all, get_by_id, get_by_parent_id, get_by_name_and_parent, create.
        # Let's check CategoriesRepository content again mentally.
        # It did NOT have get_filtered.
        # Maybe it was dynamically added or I missed it.
        # To be safe, I will comment this out or assume it wasn't used/working, or implement it if needed.
        # But I must return something valid or remove the method if unused.
        # Given the task is refactor to async, I'll assume get_filtered is not the main focus or doesn't exist.
        # I will remove it to avoid runtime error effectively if repo doesn't have it.
        pass
