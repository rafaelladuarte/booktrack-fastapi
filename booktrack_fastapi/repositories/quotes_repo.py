from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.reading_quotes import ReadingQuotes


class QuotesRepository:
    """Repositório para operações de banco de dados de citações de leitura."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_reading_id(self, reading_id: int) -> list[ReadingQuotes]:
        """Lista todas as citações de uma leitura em ordem cronológica.

        Args:
            reading_id: ID da leitura pai.

        Returns:
            Lista de instâncias de ReadingQuotes ordenadas por data de criação.
        """
        stmt = (
            select(ReadingQuotes)
            .where(ReadingQuotes.reading_id == reading_id)
            .order_by(ReadingQuotes.created_at.asc())
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, quote_id: int) -> ReadingQuotes | None:
        """Busca uma citação pelo ID primário.

        Args:
            quote_id: ID da citação.

        Returns:
            Instância de ReadingQuotes ou None se não encontrada.
        """
        stmt = select(ReadingQuotes).where(ReadingQuotes.id == quote_id)
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, reading_id: int, data: dict) -> ReadingQuotes:
        """Cria e persiste uma nova citação.

        Args:
            reading_id: ID da leitura à qual a citação pertence.
            data: Dicionário com os atributos da citação (content, page_number).

        Returns:
            A instância de ReadingQuotes criada e persistida.
        """
        quote = ReadingQuotes(reading_id=reading_id, **data)
        self.db.add(quote)
        await self.db.commit()
        await self.db.refresh(quote)
        return quote

    async def delete(self, quote_id: int) -> bool:
        """Deleta uma citação pelo ID.

        Args:
            quote_id: ID da citação a ser deletada.

        Returns:
            True se a citação foi encontrada e deletada, False caso contrário.
        """
        stmt = delete(ReadingQuotes).where(ReadingQuotes.id == quote_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0
