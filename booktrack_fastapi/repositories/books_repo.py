from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from booktrack_fastapi.models.books import Books, BooksExpandedView


class BooksRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        stmt = select(BooksExpandedView)
        return self.db.scalars(stmt).all()

    def get_by_id(self, book_id: int):
        return self.db.get(BooksExpandedView, book_id)

    def get_by_filter(self, filters):
        stmt = select(BooksExpandedView)
        conditions = []

        if filters.get('title'):
            conditions.append(BooksExpandedView.title.ilike(f'%{filters["title"]}%'))

        if filters.get('year'):
            conditions.append(
                BooksExpandedView.original_publication_year == filters['year']
            )

        if filters.get('publisher_id'):
            conditions.append(
                BooksExpandedView.publisher_id == filters['publisher_id']
            )

        if filters.get('collection_id'):
            conditions.append(
                BooksExpandedView.collection_id == filters['collection_id']
            )

        if filters.get('format_id'):
            conditions.append(BooksExpandedView.format_id == filters['format_id'])

        if filters.get('author_id'):
            conditions.append(BooksExpandedView.author_id == filters['author_id'])

        if filters.get('category_id'):
            conditions.append(
                BooksExpandedView.category_id == filters['category_id']
            )

        if filters.get('shelve_id'):
            conditions.append(BooksExpandedView.shelve_id == filters['shelve_id'])

        if conditions:
            stmt = stmt.where(*conditions)

        return self.db.scalars(stmt).all()

    def create(
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
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_by_id(
        self,
        book_id: int,
        parameters: dict,
    ):
        stmt = (
            update(Books).where(Books.id == book_id).values(**parameters)
        )
        self.db.execute(stmt)
        self.db.commit()
        return True

    def delete_by_id(self, book_id: int):
        stmt = (
            delete(Books).where(Books.id == book_id)
        )
        self.db.execute(stmt)
        self.db.commit()
        return True
