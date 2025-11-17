from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Publishers(Base):
    __tablename__ = 'publishers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    books: Mapped[list['Books']] = relationship(back_populates='publisher')  # noqa: F821
