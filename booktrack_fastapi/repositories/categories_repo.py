from sqlalchemy import select
from sqlalchemy.orm import Session

from booktrack_fastapi.models.categories import Categories


class CategoriesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        stmt = select(Categories)
        return self.db.scalars(stmt).all()

    def get_by_id(self, category_id: int):
        return self.db.get(Categories, category_id)

    def get_by_parent_id(self, parent_id: int):
        stmt = select(Categories).where(Categories.parent_id == parent_id)
        return self.db.scalars(stmt).all()

    def get_by_name_and_parent(self, name: str, parent_id: int = None):
        stmt = select(Categories).where(
            Categories.parent_id == parent_id, Categories.name == name
        )
        return self.db.scalars(stmt).all()

    def create(self, name: str, parent_id: int | None = None):
        item = Categories(name=name, parent_id=parent_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
