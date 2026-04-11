from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from booktrack_fastapi.models.books import Books


class BooksRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = select(Books).options(
            selectinload(Books.publisher),
            selectinload(Books.collection),
            selectinload(Books.format),
            selectinload(Books.author),
            selectinload(Books.category),
        )
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, book_id: int):
        stmt = select(Books).where(Books.id == book_id).options(
            selectinload(Books.publisher),
            selectinload(Books.collection),
            selectinload(Books.format),
            selectinload(Books.author),
            selectinload(Books.category),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_filter(self, filters):
        stmt = select(Books).options(
            selectinload(Books.publisher),
            selectinload(Books.collection),
            selectinload(Books.format),
            selectinload(Books.author),
            selectinload(Books.category),
        )
        conditions = []

        if filters.get('title'):
            conditions.append(Books.title.ilike(f'%{filters["title"]}%'))

        if filters.get('year'):
            conditions.append(
                Books.original_publication_year == filters['year']
            )

        if filters.get('publisher_id'):
            conditions.append(
                Books.publisher_id == filters['publisher_id']
            )

        if filters.get('collection_id'):
            conditions.append(
                Books.collection_id == filters['collection_id']
            )

        if filters.get('format_id'):
            conditions.append(Books.format_id == filters['format_id'])

        if filters.get('author_id'):
            conditions.append(Books.author_id == filters['author_id'])

        if filters.get('category_id'):
            conditions.append(
                Books.category_id == filters['category_id']
            )

        # Note: shelve_id was in original but Books model doesn't seem to have
        # direct shelve relationship except via readings? I'll ignore shelve_id
        # for now as it might need a join.

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.db.scalars(stmt)
        return result.all()

    async def create(
        self,
        parameters: dict,
    ):
        item = Books(
            title=parameters.get('title'),
            original_publication_year=parameters.get('original_publication_year'),
            total_pages=parameters.get('total_pages'),
            publisher_id=parameters.get('publisher_id'),
            collection_id=parameters.get('collection_id'),
            format_id=parameters.get('format_id'),
            author_id=parameters.get('author_id'),
            category_id=parameters.get('category_id'),
            cover_url=parameters.get('cover_url'),
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_by_id(
        self,
        book_id: int,
        parameters: dict,
    ):
        stmt = (
            update(Books).where(Books.id == book_id).values(**parameters)
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return True

    async def delete_by_id(self, book_id: int):
        stmt = (
            delete(Books).where(Books.id == book_id)
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return True
