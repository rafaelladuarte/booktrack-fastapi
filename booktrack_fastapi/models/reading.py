from datetime import datetime

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.properties import Shelves, StatusReading, Tags

table_registry_readings = registry()


readings_tags = Table(
    'readings_tags',
    table_registry_readings.metadata,
    Column('reading_id', ForeignKey('readings.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)

readings_shelves = Table(
    'readings_shelves',
    table_registry_readings.metadata,
    Column('reading_id', ForeignKey('reatings.id'), primary_key=True),
    Column('shelve_id', ForeignKey('shelves.id'), primary_key=True),
)


@table_registry_readings.mapped_as_dataclass
class Readings:
    __tablename__ = 'readings'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    status_id: Mapped[int] = mapped_column(ForeignKey('reading_status.id'))

    start_date: Mapped[datetime | None]
    end_date: Mapped[datetime | None]
    pages_read: Mapped[int | None]
    personal_goal: Mapped[str | None]
    club_date: Mapped[datetime | None]
    club_name: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    book: Mapped['Books'] = relationship(back_populates='readings')
    status: Mapped['StatusReading'] = relationship()

    tags: Mapped[list['Tags']] = relationship(secondary='readings_tag')
    shelves: Mapped[list['Shelves']] = relationship(
        secondary='reading_shelves'
    )
