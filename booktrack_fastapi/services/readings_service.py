from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.repositories.books_repo import BooksRepository
from booktrack_fastapi.repositories.readings_repo import ReadingsRepository
from booktrack_fastapi.schemas.readings import ReadingCreate, ReadingUpdate


class ReadingsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ReadingsRepository(db)
        self.books_repo = BooksRepository(db)

    async def create(self, user_id: int, data: ReadingCreate):
        """Valida relacionamentos e delega a criação de leituras para o Repositório.

        Args:
            user_id: ID do Usuário corrente em auth token.
            data: Dados estruturados via BaseModel.

        Returns:
            Objeto Readings expandido se criado com sucesso.

        Raises:
            HTTPException: Status 404 se book_id não for detectado na base de dados.
        """
        book = await self.books_repo.get_by_id(data.book_id)
        if not book:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {data.book_id} not found.',
            )

        return await self.repo.create(user_id=user_id, data=data.model_dump())

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_book_id(self, book_id: int):
        obj = await self.repo.get_by_book_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.',
            )
        return obj

    async def list_by_filter(self, filters):
        return await self.repo.get_by_filter(filters.model_dump())

    async def update_by_book_id(self, book_id: int, data: 'ReadingUpdate'):
        obj = await self.repo.get_by_book_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.',
            )

        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update_by_book_id(book_id, update_data)
