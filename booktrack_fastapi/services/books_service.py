from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers

from booktrack_fastapi.repositories.books_repo import BooksRepository
from booktrack_fastapi.repositories.categories_repo import CategoriesRepository
from booktrack_fastapi.repositories.properties_repo import PropertiesRepository
from booktrack_fastapi.schemas.books import BookCreate, BookUpdate


class BooksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = BooksRepository(db)

    async def create(self, data: 'BookCreate'):
        """Cria um novo livro validando campos obrigatórios e duplicidade.

        Args:
            data: Dados para criação do livro.

        Returns:
            O objeto Books criado.

        Raises:
            HTTPException: 400 se campos obrigatórios faltarem, se o nome for curto
                ou se o livro já existir.
        """
        if not all([data.title, data.original_publication_year, data.total_pages]):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    'Todos os parâmetros obrigatórios '
                    '(title, original_publication_year, total_pages) '
                    'devem ser preenchidos.'
                ),
            )

        title = data.title.strip()
        min_length = 10

        if len(title) < min_length:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'The name must be at least {min_length} characters.',
            )

        title_existing = await self.repo.get_by_filter({'title': title})
        if title_existing:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=f"Book '{title}' already not exists."
            )

        if data.category_id:
            categories_repo = CategoriesRepository(self.db)
            category_existing = await categories_repo.get_by_id(data.category_id)
            if not category_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Category_id {data.category_id} not exists.',
                )

        if data.publisher_id:
            publisher_existing = await PropertiesRepository(self.db, Publishers).get_by_id(
                data.publisher_id
            )
            if not publisher_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Publisher_id {data.publisher_id} not exists.',
                )

        if data.format_id:
            format_existing = await PropertiesRepository(self.db, Formats).get_by_id(data.format_id)
            if not format_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Format_id {data.format_id} not exists.',
                )

        if data.collection_id:
            collection_existing = await PropertiesRepository(self.db, Collections).get_by_id(
                data.collection_id
            )
            if not collection_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Collection_id {data.collection_id} not exists.',
                )

        return await self.repo.create(data.model_dump())

    async def list_all(self):
        """Retorna todos os livros cadastrados com seus relacionamentos.

        Returns:
            Lista de objetos Books.
        """
        return await self.repo.get_all()

    async def get_by_id(self, book_id: int):
        """Busca um livro específico pelo seu ID.

        Args:
            book_id: Identificador único do livro.

        Returns:
            O objeto Books encontrado.

        Raises:
            HTTPException: 404 se o livro não for encontrado.
        """
        obj = await self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'Book_id {book_id} not found.'
            )
        return obj

    async def list_by_filter(self, filters):
        """Lista livros aplicando filtros dinâmicos.

        Args:
            filters: Objeto com os campos de filtro.

        Returns:
            Lista de livros que atendem aos critérios.
        """
        return await self.repo.get_by_filter(filters.model_dump())

    async def update_by_id(self, book_id: int, data: 'BookUpdate'):
        """Atualiza os dados de um livro existente.

        Args:
            book_id: ID do livro a ser atualizado.
            data: Dados para atualização (campos opcionais).

        Returns:
            O objeto Books atualizado.

        Raises:
            HTTPException: 404 se o livro não for encontrado.
        """
        obj = await self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'Book_id {book_id} not found.'
            )
        return await self.repo.update_by_id(book_id, data.model_dump(exclude_unset=True))

    async def delete_by_id(self, book_id: int):
        """Remove um livro do sistema pelo seu ID.

        Args:
            book_id: ID do livro a ser removido.

        Returns:
            True se a remoção for bem-sucedida.

        Raises:
            HTTPException: 404 se o livro não for encontrado.
        """
        obj = await self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=f'Book_id {book_id} not found.'
            )
        return await self.repo.delete_by_id(book_id)
