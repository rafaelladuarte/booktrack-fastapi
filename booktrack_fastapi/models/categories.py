from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from . import Base

books_categories = Table(
    'books_categories',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
)


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
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
