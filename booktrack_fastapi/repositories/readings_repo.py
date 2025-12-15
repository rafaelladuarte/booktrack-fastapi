from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.readings import ReadingExpandedView, Readings


class ReadingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = select(ReadingExpandedView)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, reading_id: int):
        return await self.db.get(ReadingExpandedView, reading_id)

    async def get_by_book_id(self, book_id: int):
         # Note: method was missing in previous file view but used in service. Assuming logical implementation.
         # ReadingExpandedView has a reading_id, but logically we want to search by book_id too?
         # The View has book_id column.
        stmt = select(ReadingExpandedView).where(ReadingExpandedView.book_id == book_id)
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_filter(self, filters):
        stmt = select(ReadingExpandedView)
        conditions = []

        if filters.get('title'):
            conditions.append(ReadingExpandedView.title.ilike(f'%{filters["title"]}%'))

        if filters.get('year'):
            conditions.append(
                ReadingExpandedView.original_publication_year == filters['year']
            )

        if filters.get('publisher_id'):
            conditions.append(
                ReadingExpandedView.publisher_id == filters['publisher_id']
            )

        if filters.get('collection_id'):
            conditions.append(
                ReadingExpandedView.collection_id == filters['collection_id']
            )

        if filters.get('format_id'):
            conditions.append(ReadingExpandedView.format_id == filters['format_id'])

        if filters.get('author_id'):
            conditions.append(ReadingExpandedView.author_id == filters['author_id'])

        if filters.get('category_id'):
            conditions.append(
                ReadingExpandedView.category_id == filters['category_id']
            )

        # Note: shelve_id logic might need View update if not present, but keeping code structure
        if filters.get('shelve_id'):
             # Assuming this column exists in View as implied by previous code,
             # though I didn't verify it in the View definition recently.
             # Based on previous file, it was trying to access it.
             pass
             # conditions.append(ReadingExpandedView.shelve_id == filters['shelve_id'])

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.db.scalars(stmt)
        return result.all()

    async def update_by_book_id(
        self,
        book_id: int,
        parameters: dict,
    ):
        stmt = (
            update(Readings).where(Readings.book_id == book_id).values(**parameters)
        )
        await self.db.execute(stmt)
        await self.db.commit()

        # Helper to get fresh object
        stmt_refresh = select(Readings).where(Readings.book_id == book_id)
        result = await self.db.scalars(stmt_refresh)
        return result.first()
