from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from booktrack_fastapi.repositories.authors_repo import AuthorsRepository
from booktrack_fastapi.schemas.authors import AuthorCreate, AuthorUpdate
from booktrack_fastapi.utility.tools import item_to_dict


class AuthorsService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuthorsRepository(db)

    def list_all(self):
        items = self.repo.get_all()
        return [item_to_dict(i) for i in items]

    def get_by_id(self, author_id: int):
        obj = self.repo.get_by_id(author_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Author_id {author_id} not found.',
            )
        return item_to_dict(obj)

    def create(self, data: AuthorCreate):
        return item_to_dict(self.repo.create(data.model_dump()))

    def update(self, author_id: int, data: AuthorUpdate):
        obj = self.repo.get_by_id(author_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Author_id {author_id} not found.',
            )
        updated_obj = self.repo.update_by_id(
            author_id, data.model_dump(exclude_unset=True)
        )
        return item_to_dict(updated_obj)

    def delete(self, author_id: int):
        obj = self.repo.get_by_id(author_id)
        if not obj:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Author_id {author_id} not found.',
            )
        self.repo.delete_by_id(author_id)
