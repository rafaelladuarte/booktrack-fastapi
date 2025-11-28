from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from booktrack_fastapi.models.authors import Authors


class AuthorsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        stmt = select(Authors)
        return self.db.scalars(stmt).all()

    def get_by_id(self, author_id: int):
        return self.db.get(Authors, author_id)

    def create(self, parameters: dict):
        item = Authors(**parameters)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_by_id(self, author_id: int, parameters: dict):
        stmt = update(Authors).where(Authors.id == author_id).values(**parameters)
        self.db.execute(stmt)
        self.db.commit()
        return self.get_by_id(author_id)

    def delete_by_id(self, author_id: int):
        stmt = delete(Authors).where(Authors.id == author_id)
        self.db.execute(stmt)
        self.db.commit()
