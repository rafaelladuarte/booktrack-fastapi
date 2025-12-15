from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.repositories.authors_repo import AuthorsRepository
from booktrack_fastapi.schemas.authors import AuthorCreate, AuthorUpdate
from booktrack_fastapi.utility.tools import item_to_dict


class AuthorsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthorsRepository(db)

    async def list_all(self):
        items = await self.repo.get_all()
        return [item_to_dict(i) for i in items]

    async def get_by_id(self, author_id: int):
        obj = await self.repo.get_by_id(author_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Author_id {author_id} not found.',
            )
        return item_to_dict(obj)

    async def create(self, data: AuthorCreate):
        result = await self.repo.create(data.model_dump())
        return item_to_dict(result)

    async def update(self, author_id: int, data: AuthorUpdate):
        obj = await self.repo.get_by_id(author_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Author_id {author_id} not found.',
            )
        updated_obj = await self.repo.update_by_id(
            author_id, data.model_dump(exclude_unset=True)
        )
        return item_to_dict(updated_obj)

    async def delete(self, author_id: int):
        obj = await self.repo.get_by_id(author_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Author_id {author_id} not found.',
            )
        await self.repo.delete_by_id(author_id)
