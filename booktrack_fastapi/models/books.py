from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from booktrack_fastapi.models.associations import (
    books_authors,
    books_categories,
)

from .base import Base


class Books(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)

    publisher_id: Mapped[int | None] = mapped_column(
        ForeignKey('publishers.id')
    )
    collection_id: Mapped[int | None] = mapped_column(
        ForeignKey('collections.id')
    )
    format_id: Mapped[int | None] = mapped_column(ForeignKey('formats.id'))
    category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'))
    author_id: Mapped[int | None] = mapped_column(ForeignKey('authors.id'))

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_publication_year: Mapped[int | None]
    total_pages: Mapped[int | None]
    cover_url: Mapped[str | None] = mapped_column(Text)

    publisher: Mapped['Publishers'] = relationship(  # noqa: F821
        back_populates='books'
    )
    collection: Mapped['Collections'] = relationship(  # noqa: F821
        back_populates='books'
    )
    format: Mapped['Formats'] = relationship(  # noqa: F821
        back_populates='books'
    )

    authors: Mapped[list['Authors']] = relationship(  # noqa: F821
        secondary=books_authors, back_populates='books'
    )

    categories: Mapped[list['Categories']] = relationship(  # noqa: F821
        secondary=books_categories, back_populates='books'
    )

    readings: Mapped[list['Readings']] = relationship(  # noqa: F821
        back_populates='book'
    )
