from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from booktrack_fastapi.models.books import Books

table_registry_categories = registry()

books_categories = Table(
    'books_categories',
    table_registry_categories.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
)


@table_registry_categories.mapped_as_dataclass
class Categories:
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'))

    parent: Mapped['Categories'] = relationship(
        'Categories', remote_side=[id], back_populates='subcategories'
    )
    subcategories: Mapped[list['Categories']] = relationship(
        'Categories', back_populates='parent'
    )

    books: Mapped[list['Books']] = relationship(
        secondary=books_categories, back_populates='categories'
    )
