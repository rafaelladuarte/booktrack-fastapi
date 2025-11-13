from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from . import Base


readings_tags = Table(
    'readings_tags',
    Base.metadata,
    Column('reading_id', ForeignKey('readings.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)

readings_shelves = Table(
    'readings_shelves',
    Base.metadata,
    Column('reading_id', ForeignKey('readings.id'), primary_key=True),
    Column('shelve_id', ForeignKey('shelves.id'), primary_key=True),
)


class Readings(Base):
    __tablename__ = 'readings'

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    status_id: Mapped[int] = mapped_column(ForeignKey('reading_status.id'))

    start_date: Mapped[datetime | None]
    end_date: Mapped[datetime | None]
    pages_read: Mapped[int | None]
    personal_goal: Mapped[str | None]
    club_date: Mapped[datetime | None]
    club_name: Mapped[str | None]

    book_id: Mapped['Books'] = relationship(back_populates='readings')
    status_id: Mapped['StatusReading'] = relationship()

    tags: Mapped[list['Tags']] = relationship(secondary='readings_tags')
    shelves: Mapped[list['Shelves']] = relationship(
        secondary='reading_shelves'
    )
