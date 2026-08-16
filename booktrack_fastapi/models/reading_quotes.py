import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ReadingQuotes(Base):
    """Modelo de citações e notas de leitura.

    Cada citação está associada a uma leitura específica (1-para-N).
    Ao deletar uma leitura, todas as suas citações são removidas em cascata
    via ForeignKey ondelete='CASCADE'.
    """

    __tablename__ = 'reading_quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    reading_id: Mapped[int] = mapped_column(
        ForeignKey('readings.id', ondelete='CASCADE'), nullable=False
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    reading: Mapped['Readings'] = relationship(back_populates='quotes')  # noqa: F821
