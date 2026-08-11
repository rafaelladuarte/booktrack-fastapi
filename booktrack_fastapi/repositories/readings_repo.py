from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.readings import Readings


class ReadingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        """Lista todas as leituras com carregamento de livro, status, tags e estantes.

        Returns:
            Lista de instâncias de Readings.
        """
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
        """Busca uma leitura por ID com todos os relacionamentos expandidos.

        Args:
            reading_id: ID primário da leitura.

        Returns:
            Instância de Readings ou None.
        """
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
        """Busca o registro de leitura vinculado a um ID de livro específico.

        Args:
            book_id: ID do livro.

        Returns:
            Instância de Readings ou None.
        """
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
        """Filtra leituras por status ou nome do clube do livro.

        Args:
            filters: Dicionário com critérios de busca.

        Returns:
            Lista de leituras filtradas.
        """
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
        """Atualiza dados de leitura vinculados a um livro específico.

        Args:
            book_id: ID do livro.
            parameters: Atributos a serem modificados.

        Returns:
            A instância de Readings atualizada.
        """
        reading = await self.get_by_book_id(book_id)
        if not reading:
            return None

        tag_ids = parameters.pop('tag_ids', None)
        shelf_ids = parameters.pop('shelf_ids', None)

        if parameters:
            stmt = update(Readings).where(Readings.book_id == book_id).values(**parameters)
            await self.db.execute(stmt)

        if tag_ids is not None:
            if tag_ids:
                from booktrack_fastapi.models.tags import Tags
                stmt_tags = select(Tags).where(Tags.id.in_(tag_ids))
                tags = await self.db.scalars(stmt_tags)
                reading.tags = list(tags.all())
            else:
                reading.tags = []

        if shelf_ids is not None:
            if shelf_ids:
                from booktrack_fastapi.models.shelves import Shelves
                stmt_shelves = select(Shelves).where(Shelves.id.in_(shelf_ids))
                shelves = await self.db.scalars(stmt_shelves)
                reading.shelves = list(shelves.all())
            else:
                reading.shelves = []

        if tag_ids is not None or shelf_ids is not None:
            # Necessário adicionar à sessão para persistir as relações do ORM
            self.db.add(reading)
            
        await self.db.commit()

        # Helper to get fresh object
        return await self.get_by_book_id(book_id)
