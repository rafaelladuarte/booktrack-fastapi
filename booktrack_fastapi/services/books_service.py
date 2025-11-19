from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from booktrack_fastapi.repositories.books_repo import BooksRepository
from booktrack_fastapi.schemas.books import BookCreate
from booktrack_fastapi.utility.tools import item_to_dict


class BooksService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BooksRepository(db)

    def create(self, data: BookCreate):
        title = data.title.strip()
        min_length = 10

        if len(title) < min_length:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'O nome deve ter pelo menos {min_length} caracteres.',
            )
        existing = self.repo.get_by_filter(
            title=title,
            original_publication_year=data.original_publication_year,
            total_pages=data.total_pages,
            publisher_id=data.publisher_id,
            collection_id=data.collection_id,
            format_id=data.format_id,
            author_id=data.author_id,
            category_id=data.category_id,
        )

        if existing:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Livro '{title}' já existe na biblioteca.",
            )

        return self.repo.create(data.model_dump())

    def list_all(self):
        items = self.repo.get_all()
        return [item_to_dict(i) for i in items]

    def get_by_id(self, book_id: int):
        obj = self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id={book_id} não encontrada.',
            )
        return item_to_dict(obj)

    def list_by_filter(self, filters):
        items = self.repo.get_by_filter(filters.model_dump())
        return [item_to_dict(i) for i in items]
