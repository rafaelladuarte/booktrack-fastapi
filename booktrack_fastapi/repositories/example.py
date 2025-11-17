from app.models.book import Book
from sqlalchemy.orm import Session


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, author: str) -> Book:
        book = Book(title=title, author=author)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get(self, book_id: int) -> Book | None:
        return self.db.query(Book).filter(Book.id == book_id).first()
