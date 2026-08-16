from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from booktrack_fastapi.models.associations import readings_shelves, readings_tags
from booktrack_fastapi.models.authors import Authors
from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.categories import Categories
from booktrack_fastapi.models.readings import Readings


class BooksRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        """Executa query para retornar todos os livros com seus relacionamentos.

        Returns:
            Lista de instâncias de Books.
        """
        stmt = select(Books).options(
            selectinload(Books.publisher),
            selectinload(Books.collection),
            selectinload(Books.format),
            selectinload(Books.author),
            selectinload(Books.category),
        )
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, book_id: int):
        """Busca um livro por ID carregando antecipadamente todos os relacionamentos.

        Args:
            book_id: ID primário do livro.

        Returns:
            Instância de Books ou None.
        """
        stmt = (
            select(Books)
            .where(Books.id == book_id)
            .options(
                selectinload(Books.publisher),
                selectinload(Books.collection),
                selectinload(Books.format),
                selectinload(Books.author),
                selectinload(Books.category),
                selectinload(Books.readings).selectinload(Readings.status),
                selectinload(Books.readings).selectinload(Readings.tags),
                selectinload(Books.readings).selectinload(Readings.shelves),
                selectinload(Books.readings).selectinload(Readings.quotes),
            )
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_filter(self, filters: dict):
        """Busca livros no banco de dados aplicando filtros dinâmicos.

        Args:
            filters: Dicionário contendo os campos de filtro.
                Suporta: title, year, publisher_id/publish_id, collection_id,
                format_id, author_id, category_id, shelve_id, tag_id e status_id.

        Returns:
            Lista de objetos Books carregados com relacionamentos.
        """
        stmt = select(Books).options(
            selectinload(Books.publisher),
            selectinload(Books.collection),
            selectinload(Books.format),
            selectinload(Books.author),
            selectinload(Books.category),
        )

        # Filtros que requerem JOIN na tabela Readings
        needs_readings_join = any(filters.get(k) for k in ('shelve_id', 'tag_id', 'status_id'))
        if needs_readings_join:
            stmt = stmt.join(Readings, Readings.book_id == Books.id)

        if filters.get('shelve_id'):
            stmt = (
                stmt
                .join(readings_shelves, readings_shelves.c.reading_id == Readings.id)
                .where(readings_shelves.c.shelf_id == filters['shelve_id'])
            )

        if filters.get('tag_id'):
            stmt = (
                stmt
                .join(readings_tags, readings_tags.c.reading_id == Readings.id)
                .where(readings_tags.c.tag_id == filters['tag_id'])
            )

        if filters.get('status_id'):
            stmt = stmt.where(Readings.status_id == filters['status_id'])

        if needs_readings_join:
            stmt = stmt.distinct()

        conditions = []

        if filters.get('title'):
            conditions.append(Books.title.ilike(f'%{filters["title"]}%'))

        if filters.get('year'):
            conditions.append(Books.original_publication_year == filters['year'])

        # Normaliza inconsistência entre schema (publish_id) e repo (publisher_id)
        publisher_id = filters.get('publisher_id') or filters.get('publish_id')
        if publisher_id:
            conditions.append(Books.publisher_id == publisher_id)

        if filters.get('collection_id'):
            conditions.append(Books.collection_id == filters['collection_id'])

        if filters.get('format_id'):
            conditions.append(Books.format_id == filters['format_id'])

        if filters.get('author_id'):
            conditions.append(Books.author_id == filters['author_id'])

        needs_authors_join = any(filters.get(k) for k in ('author_name', 'author_country', 'author_gender', 'q'))
        if needs_authors_join:
            stmt = stmt.outerjoin(Authors, Books.author_id == Authors.id)
            if filters.get('author_name'):
                conditions.append(Authors.name.ilike(f'%{filters["author_name"]}%'))
            if filters.get('author_country'):
                conditions.append(Authors.country_of_origin.ilike(filters['author_country']))
            if filters.get('author_gender'):
                conditions.append(Authors.gender == filters['author_gender'])

        if filters.get('q'):
            from sqlalchemy import or_
            q_term = f'%{filters["q"]}%'
            conditions.append(or_(Books.title.ilike(q_term), Authors.name.ilike(q_term)))

        if filters.get('category_id'):
            descendant_ids = await self._get_descendant_category_ids(filters['category_id'])
            conditions.append(Books.category_id.in_(descendant_ids))

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.db.scalars(stmt)
        return result.all()

    async def _get_descendant_category_ids(self, category_id: int) -> list[int]:
        """Retorna o ID da categoria + todos os IDs descendentes (filhos e netos)."""
        all_ids = [category_id]

        # Nível 2: filhos diretos
        stmt = select(Categories.id).where(Categories.parent_id == category_id)
        result = await self.db.scalars(stmt)
        children_ids = list(result.all())
        all_ids.extend(children_ids)

        # Nível 3: netos (filhos dos filhos)
        if children_ids:
            stmt = select(Categories.id).where(Categories.parent_id.in_(children_ids))
            result = await self.db.scalars(stmt)
            grandchildren_ids = list(result.all())
            all_ids.extend(grandchildren_ids)

        return all_ids

    async def create(
        self,
        parameters: dict,
    ):
        """Persiste um novo livro no banco de dados.

        Args:
            parameters: Dicionário com os atributos do livro.

        Returns:
            A instância de Books recém-criada.
        """
        item = Books(
            title=parameters.get('title'),
            original_publication_year=parameters.get('original_publication_year'),
            total_pages=parameters.get('total_pages'),
            publisher_id=parameters.get('publisher_id'),
            collection_id=parameters.get('collection_id'),
            format_id=parameters.get('format_id'),
            author_id=parameters.get('author_id'),
            category_id=parameters.get('category_id'),
            cover_url=parameters.get('cover_url'),
            synopsis=parameters.get('synopsis'),
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_by_id(
        self,
        book_id: int,
        parameters: dict,
    ):
        """Atualiza campos específicos de um livro por ID.

        Args:
            book_id: ID do livro.
            parameters: Dicionário com campos e valores a atualizar.

        Returns:
            True se a operação foi executada.
        """
        stmt = update(Books).where(Books.id == book_id).values(**parameters)
        await self.db.execute(stmt)
        await self.db.commit()
        return True

    async def delete_by_id(self, book_id: int):
        """Remove permanentemente um livro do banco de dados e suas dependências.

        Args:
            book_id: ID do livro a ser deletado.

        Returns:
            True se a operação foi executada.
        """
        # Deletar das tabelas de associação do livro
        from booktrack_fastapi.models.associations import books_authors, books_categories, readings_tags, readings_shelves
        await self.db.execute(delete(books_authors).where(books_authors.c.book_id == book_id))
        await self.db.execute(delete(books_categories).where(books_categories.c.book_id == book_id))

        # Obter leituras
        stmt_readings = select(Readings.id).where(Readings.book_id == book_id)
        result = await self.db.execute(stmt_readings)
        reading_ids = result.scalars().all()

        if reading_ids:
            # Remover associações de tags e prateleiras
            await self.db.execute(delete(readings_tags).where(readings_tags.c.reading_id.in_(reading_ids)))
            await self.db.execute(delete(readings_shelves).where(readings_shelves.c.reading_id.in_(reading_ids)))
            # Remover leituras
            await self.db.execute(delete(Readings).where(Readings.book_id == book_id))

        stmt = delete(Books).where(Books.id == book_id)
        await self.db.execute(stmt)
        await self.db.commit()
        return True
