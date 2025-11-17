from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from booktrack_fastapi.models.associations import readings_tags

from .base import Base


class Tags(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    readings: Mapped[list['Readings']] = relationship(  # noqa: F821
        secondary=readings_tags, back_populates='tags'
    )
