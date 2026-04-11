from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.repositories.readings_repo import ReadingsRepository
from booktrack_fastapi.schemas.readings import ReadingUpdate


class ReadingsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ReadingsRepository(db)

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_book_id(self, book_id: int):
        obj = await self.repo.get_by_book_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.',
            )
        return obj

    async def list_by_filter(self, filters):
        return await self.repo.get_by_filter(filters.model_dump())

    async def update_by_book_id(self, book_id: int, data: 'ReadingUpdate'):
        obj = await self.repo.get_by_book_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.',
            )

        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update_by_book_id(book_id, update_data)
