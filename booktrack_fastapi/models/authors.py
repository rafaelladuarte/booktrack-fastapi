from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from booktrack_fastapi.models.associations import books_authors

from .base import Base


class Authors(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[str | None] = mapped_column(String(1))
    country_of_origin: Mapped[str | None] = mapped_column(String(255))

    books: Mapped[list['Books']] = relationship(  # noqa: F821
        secondary=books_authors, back_populates='authors'
    )
