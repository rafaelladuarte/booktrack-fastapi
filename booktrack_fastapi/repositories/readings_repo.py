from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.readings import Readings


class ReadingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = select(Readings).options(
            selectinload(Readings.status),
            selectinload(Readings.tags),
            selectinload(Readings.shelves),
            selectinload(Readings.book).options(
                selectinload(Books.author),
                selectinload(Books.publisher),
                selectinload(Books.collection),
                selectinload(Books.format),
                selectinload(Books.category),
            ),
        )
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, reading_id: int):
        stmt = (
            select(Readings)
            .where(Readings.id == reading_id)
            .options(
                selectinload(Readings.status),
                selectinload(Readings.tags),
                selectinload(Readings.shelves),
                selectinload(Readings.book).options(
                    selectinload(Books.author),
                    selectinload(Books.publisher),
                    selectinload(Books.collection),
                    selectinload(Books.format),
                    selectinload(Books.category),
                ),
            )
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_book_id(self, book_id: int):
        stmt = (
            select(Readings)
            .where(Readings.book_id == book_id)
            .options(
                selectinload(Readings.status),
                selectinload(Readings.tags),
                selectinload(Readings.shelves),
                selectinload(Readings.book).options(
                    selectinload(Books.author),
                    selectinload(Books.publisher),
                    selectinload(Books.collection),
                    selectinload(Books.format),
                    selectinload(Books.category),
                ),
            )
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, user_id: int, data: dict):
        """Cria e persiste uma nova leitura.

        Args:
            user_id: ID do usuário autenticado no sistema.
            data: Dicionário com os atributos da leitura criados no request body.

        Returns:
            O objeto Readings carregado com todos os relacionamentos necessários.
        """
        reading = Readings(**data)
        self.db.add(reading)
        await self.db.commit()
        await self.db.refresh(reading)

        # Recarregar para trazer relacionamentos via selectinload
        return await self.get_by_id(reading.id)

    async def get_by_filter(self, filters):
        stmt = select(Readings).options(
            selectinload(Readings.status),
            selectinload(Readings.tags),
            selectinload(Readings.shelves),
            selectinload(Readings.book).options(
                selectinload(Books.author),
                selectinload(Books.publisher),
                selectinload(Books.collection),
                selectinload(Books.format),
                selectinload(Books.category),
            ),
        )
        conditions = []

        if filters.get('status_id'):
            conditions.append(Readings.status_id == filters['status_id'])

        if filters.get('club_name'):
            conditions.append(Readings.club_name.ilike(f'%{filters["club_name"]}%'))

        # If we need title filter, we must join Books
        # But ReadingQuery (schema) only had status_id and club_name.
        # The repo get_by_filter previously had title/year etc from ExpandedView.
        # I'll keep it simple for now based on ReadingQuery.

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.db.scalars(stmt)
        return result.all()

    async def update_by_book_id(
        self,
        book_id: int,
        parameters: dict,
    ):
        stmt = update(Readings).where(Readings.book_id == book_id).values(**parameters)
        await self.db.execute(stmt)
        await self.db.commit()

        # Helper to get fresh object
        stmt_refresh = select(Readings).where(Readings.book_id == book_id)
        result = await self.db.scalars(stmt_refresh)
        return result.first()
