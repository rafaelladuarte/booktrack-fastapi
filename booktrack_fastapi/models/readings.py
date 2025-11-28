import datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
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

    book: Mapped['Books'] = relationship(back_populates='readings')  # noqa: F821
    status: Mapped['ReadingStatus'] = relationship(back_populates='readings')  # noqa: F821

    tags: Mapped[list['Tags']] = relationship(  # noqa: F821
        secondary=readings_tags, back_populates='readings'
    )

    shelves: Mapped[list['Shelves']] = relationship(  # noqa: F821
        secondary=readings_shelves, back_populates='readings'
    )


class ReadingExpandedView(Base):
    __tablename__ = 'readings_expanded_view'
    __table_args__ = {'info': {'is_view': True}}

    reading_id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime.date | None]
    end_date: Mapped[datetime.date | None]
    pages_read: Mapped[int | None]
    personal_goal: Mapped[str | None]
    club_date: Mapped[datetime.date | None]
    club_name: Mapped[str | None]
    updated_at: Mapped[datetime.datetime]

    status_id: Mapped[int]
    status_name: Mapped[str]

    book_id: Mapped[int]
    title: Mapped[str]
    original_publication_year: Mapped[int | None]
    total_pages: Mapped[int | None]
    cover_url: Mapped[str | None]

    author_id: Mapped[int | None]
    author_name: Mapped[str | None]
    author_gender: Mapped[str | None]
    author_country: Mapped[str | None]

    publisher_id: Mapped[int | None]
    publisher_name: Mapped[str | None]

    collection_id: Mapped[int | None]
    collection_name: Mapped[str | None]

    format_id: Mapped[int | None]
    format_name: Mapped[str | None]

    category_id: Mapped[int | None]
    category_name: Mapped[str | None]
    category_parent_id: Mapped[int | None]

    reading_tags: Mapped[str | None]
    reading_shelves: Mapped[str | None]
