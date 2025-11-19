from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from booktrack_fastapi.models.associations import books_categories
from booktrack_fastapi.models.base import Base


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id'), nullable=True
    )

    parent: Mapped['Categories | None'] = relationship(
        remote_side='Categories.id', back_populates='children'
    )

    children: Mapped[list['Categories']] = relationship(back_populates='parent')

    books: Mapped[list['Books']] = relationship(  # noqa: F821
        secondary=books_categories, back_populates='categories'
    )
