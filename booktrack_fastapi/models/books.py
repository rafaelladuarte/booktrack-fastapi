from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from booktrack_fastapi.models.authors import Authors
from booktrack_fastapi.models.categories import Categories
from booktrack_fastapi.models.properties import (
    Collections,
    Formats,
    Publishers,
)
from booktrack_fastapi.models.reading import Readings

table_registry_books = registry()


@table_registry_books.mapped_as_dataclass
class Books:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    original_publication_year: Mapped[int | None]
    total_pages: Mapped[int | None]
    cover_url: Mapped[str | None] = mapped_column(Text)

    publisher_id: Mapped[int | None] = mapped_column(
        ForeignKey('publishers.id')
    )
    collection_id: Mapped[int | None] = mapped_column(
        ForeignKey('collections.id')
    )
    formato_id: Mapped[int | None] = mapped_column(ForeignKey('formats.id'))

    publisher_id: Mapped['Publishers'] = relationship(back_populates='books')
    collection_id: Mapped['Collections'] = relationship(back_populates='books')
    format_id: Mapped['Formats'] = relationship(back_populates='books')

    author_id: Mapped[list['Authors']] = relationship(
        secondary='books_authors', back_populates='books'
    )
    categor_id: Mapped[list['Categories']] = relationship(
        secondary='books_categories', back_populates='books'
    )
    readings: Mapped[list['Readings']] = relationship(back_populates='books')
