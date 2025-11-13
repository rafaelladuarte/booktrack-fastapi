from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from . import Base

books_authors = Table(
    'books_authors',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('auth_id', ForeignKey('authors.id'), primary_key=True),
)


class Authors(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    gender: Mapped[str | None] = mapped_column(String(1))
    country_of_origin: Mapped[str | None] = mapped_column(String)

    books: Mapped[list['Books']] = relationship(
        secondary=books_authors, back_populates='authors'
    )
