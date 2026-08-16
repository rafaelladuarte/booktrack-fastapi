from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.repositories.quotes_repo import QuotesRepository
from booktrack_fastapi.repositories.readings_repo import ReadingsRepository
from booktrack_fastapi.schemas.quotes import QuoteCreate


class QuotesService:
    """Service para orquestração de lógica de negócio de citações de leitura."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = QuotesRepository(db)
        self.readings_repo = ReadingsRepository(db)

    async def create(self, reading_id: int, data: QuoteCreate):
        """Valida a leitura e cria a nova citação.

        Args:
            reading_id: ID da leitura à qual a citação pertencerá.
            data: Dados da citação validados pelo schema QuoteCreate.

        Returns:
            A instância de ReadingQuotes criada.

        Raises:
            HTTPException: 404 se a leitura não for encontrada.
        """
        reading = await self.readings_repo.get_by_id(reading_id)
        if not reading:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Reading {reading_id} not found.',
            )
        return await self.repo.create(
            reading_id=reading_id,
            data=data.model_dump(exclude_unset=True),
        )

    async def delete(self, quote_id: int) -> None:
        """Deleta uma citação, lançando 404 se não for encontrada.

        Args:
            quote_id: ID da citação a ser deletada.

        Raises:
            HTTPException: 404 se a citação não for encontrada.
        """
        deleted = await self.repo.delete(quote_id)
        if not deleted:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Quote {quote_id} not found.',
            )
