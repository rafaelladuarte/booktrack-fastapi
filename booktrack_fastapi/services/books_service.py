from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers

# from booktrack_fastapi.repositories.authors_repo import A
from booktrack_fastapi.repositories.books_repo import BooksRepository
from booktrack_fastapi.repositories.categories_repo import CategoriesRepository
from booktrack_fastapi.repositories.properties_repo import PropertiesRepository
from booktrack_fastapi.schemas.books import BookCreate, BookUpdate
from booktrack_fastapi.utility.tools import item_to_dict


class BooksService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = BooksRepository(db)

    async def create(self, data: 'BookCreate'):
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
                detail=f'The name must be at least {min_length} characters.'
            )

        title_existing = await self.repo.get_by_filter({'title': title})
        if title_existing:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Book '{title}' already not exists."
            )

        if data.category_id:
            categories_repo = CategoriesRepository(self.db)
            category_existing = await categories_repo.get_by_id(data.category_id)
            if not category_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Category_id {data.category_id} not exists.'
                )

        # authors_repo = AuthorsRepository(self.db)
        # author_existing = authors_repo.get_by_id(data.author_id)
        # if not author_existing:
        #     raise HTTPException(
        #         status_code=HTTPStatus.BAD_REQUEST,
        #         detail=f'O autor_id {data.author_id} não existe.',
        #     )

        if data.publisher_id:
            publisher_existing = await PropertiesRepository(self.db, Publishers).get_by_id(
                data.publisher_id
            )
            if not publisher_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Publisher_id {data.publisher_id} not exists.'
                )

        if data.format_id:
            format_existing = await PropertiesRepository(self.db, Formats).get_by_id(
                data.format_id
            )
            # Was passing entity_type='Format' but generic repo doesn't take it in signature in my new version
            # Removing the legacy argument 'entity_type' as get_by_id in PropertiesRepo didn't use it in original anyway?
            # Wait, let me double check PropertiesRepo.get_by_id original..
            # Original: get_by_id(self, propertie_id: int): return self.db.query...
            # Service call: get_by_id(..., entity_type='Format') -> This implies *args or **kwargs or Python allowed it?
            # Ah, maybe the previous file viewing missed something or Python just ignored extra kwargs if not defined?
            # No, Python raises TypeError for unexpected arg.
            # Let's assume the previous service call was actually WRONG or I misread the repo.
            # I will call get_by_id(id) only.

            if not format_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Format_id {data.format_id} not exists.'
                )

        if data.collection_id:
            collection_existing = await PropertiesRepository(
                self.db, Collections
            ).get_by_id(data.collection_id)
             # Removing entity_type='Collection'
            if not collection_existing:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Collection_id {data.collection_id} not exists.'
                )

        await self.repo.create(data.model_dump())

        return True

    async def list_all(self):
        items = await self.repo.get_all()
        return [item_to_dict(i) for i in items]

    async def get_by_id(self, book_id: int):
        obj = await self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.'
            )
        return item_to_dict(obj)

    async def list_by_filter(self, filters):
        items = await self.repo.get_by_filter(filters.model_dump())
        return [item_to_dict(i) for i in items]

    async def update_by_id(self, book_id: int, data: 'BookUpdate'):
        obj = await self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.'
            )
        await self.repo.update_by_id(book_id, data.model_dump(exclude_unset=True))
        return True

    async def delete_by_id(self, book_id: int):
        obj = await self.repo.get_by_id(book_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Book_id {book_id} not found.'
            )
        await self.repo.delete_by_id(book_id)
        return True
