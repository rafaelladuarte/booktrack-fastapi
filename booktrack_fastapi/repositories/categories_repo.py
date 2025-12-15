from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.categories import Categories


class CategoriesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = select(Categories)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, category_id: int):
        return await self.db.get(Categories, category_id)

    async def get_by_parent_id(self, parent_id: int):
        stmt = select(Categories).where(Categories.parent_id == parent_id)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_name_and_parent(self, name: str, parent_id: int = None):
        stmt = select(Categories).where(
            Categories.parent_id == parent_id, Categories.name == name
        )
        result = await self.db.scalars(stmt)
        return result.all()

    async def create(self, name: str, parent_id: int | None = None):
        item = Categories(name=name, parent_id=parent_id)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item
