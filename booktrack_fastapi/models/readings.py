import datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from booktrack_fastapi.models.associations import (
    readings_shelves,
    readings_tags,
)

from .base import Base


class Readings(Base):
    __tablename__ = 'readings'

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    status_id: Mapped[int] = mapped_column(ForeignKey('reading_status.id'))

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    start_date: Mapped[datetime.date | None] = mapped_column(Date)
    end_date: Mapped[datetime.date | None] = mapped_column(Date)
    pages_read: Mapped[int | None] = mapped_column(Integer)
    personal_goal: Mapped[str | None] = mapped_column(String(255))
    club_date: Mapped[datetime.date | None] = mapped_column(Date)
    club_name: Mapped[str | None] = mapped_column(String(255))
    review: Mapped[str | None] = mapped_column(Text)

    book: Mapped['Books'] = relationship(back_populates='readings')  # noqa: F821
    status: Mapped['ReadingStatus'] = relationship(back_populates='readings')  # noqa: F821

    tags: Mapped[list['Tags']] = relationship(  # noqa: F821
        secondary=readings_tags, back_populates='readings'
    )

    shelves: Mapped[list['Shelves']] = relationship(  # noqa: F821
        secondary=readings_shelves, back_populates='readings'
    )
