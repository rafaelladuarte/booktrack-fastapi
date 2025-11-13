from sqlalchemy.orm import Mapped, mapped_column, registry

from . import Base


class Properties(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Publishers(Properties):
    __tablename__ = 'publishers'


class Formats(Properties):
    __tablename__ = 'formats'


class Collections(Properties):
    __tablename__ = 'collections'


class StatusReading(Properties):
    __tablename__ = 'reading_status'

class Tags(Properties):
    __tablename__ = 'tags'


class Shelves(Properties):
    __tablename__ = 'shelves'
