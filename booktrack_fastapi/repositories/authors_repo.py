from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.authors import Authors


class AuthorsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = select(Authors)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, author_id: int):
        return await self.db.get(Authors, author_id)

    async def create(self, parameters: dict):
        item = Authors(**parameters)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_by_id(self, author_id: int, parameters: dict):
        stmt = update(Authors).where(Authors.id == author_id).values(**parameters)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_by_id(author_id)

    async def delete_by_id(self, author_id: int):
        stmt = delete(Authors).where(Authors.id == author_id)
        await self.db.execute(stmt)
        await self.db.commit()
