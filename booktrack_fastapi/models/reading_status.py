from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ReadingStatus(Base):
    __tablename__ = 'reading_status'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    readings: Mapped[list['Readings']] = relationship(back_populates='status')  # noqa: F821
