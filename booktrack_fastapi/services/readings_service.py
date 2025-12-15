from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.repositories.readings_repo import ReadingsRepository
from booktrack_fastapi.schemas.readings import ReadingUpdate
from booktrack_fastapi.utility.tools import item_to_dict


class ReadingsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ReadingsRepository(db)

    async def list_all(self):
        items = await self.repo.get_all()
        return [item_to_dict(i) for i in items]

    async def get_by_book_id(self, book_id: int):
        obj = await self.repo.get_by_book_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.',
            )
        return item_to_dict(obj)

    async def list_by_filter(self, filters):
        items = await self.repo.get_by_filter(filters.model_dump())
        return [item_to_dict(i) for i in items]

    async def update_by_book_id(self, book_id: int, data: 'ReadingUpdate'):
        obj = await self.repo.get_by_book_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.',
            )

        update_data = data.model_dump(exclude_unset=True)
        await self.repo.update_by_book_id(book_id, update_data)
        return True
