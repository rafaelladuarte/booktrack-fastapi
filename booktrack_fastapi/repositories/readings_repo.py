from sqlalchemy import select, update
from sqlalchemy.orm import Session

from booktrack_fastapi.models.readings import Readings, ReadingExpandedView


class ReadingsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        stmt = select(ReadingExpandedView)
        return self.db.scalars(stmt).all()

    def get_by_id(self, reading_id: int):
        return self.db.get(ReadingExpandedView, reading_id)

    def get_by_filter(self, filters):
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

        if filters.get('shelve_id'):
            conditions.append(ReadingExpandedView.shelve_id == filters['shelve_id'])

        if conditions:
            stmt = stmt.where(*conditions)

        return self.db.scalars(stmt).all()

    def update_by_book_id(
        self,
        book_id: int,
        parameters: dict,
    ):
        stmt = (
            update(Readings).where(Readings.book_id == book_id).values(**parameters)
        )
        self.db.execute(stmt)
        self.db.commit()
        return self.db.get(Readings, book_id)