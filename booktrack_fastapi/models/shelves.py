from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import readings_shelves
from .base import Base


class Shelves(Base):
    __tablename__ = 'shelves'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    readings: Mapped[list['Readings']] = relationship(  # noqa: F821
        secondary=readings_shelves, back_populates='shelves'
    )
