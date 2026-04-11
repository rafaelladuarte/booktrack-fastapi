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
                detail=f'The category name must be at least {min_length} characters.',
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
        """Lista categorias aplicando filtros opcionais.

        Args:
            **filters: Objeto com os parâmetros de filtro (ex: parent_id).

        Returns:
            Lista de categorias que atendem aos filtros informados.
        """
        return await self.repo.get_filtered(**filters)
