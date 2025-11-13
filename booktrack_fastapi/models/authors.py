from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from booktrack_fastapi.models.books import Books

table_registry_authors = registry()

books_authors = Table(
    'books_authors',
    table_registry_authors.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('auth_id', ForeignKey('authors.id'), primary_key=True),
)


@table_registry_authors.mapped_as_dataclass
class Authors:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    gender: Mapped[str | None] = mapped_column(String(1))
    country_of_origin: Mapped[str | None] = mapped_column(String)

    books: Mapped[list['Books']] = relationship(
        secondary=books_authors, back_populates='authors'
    )
