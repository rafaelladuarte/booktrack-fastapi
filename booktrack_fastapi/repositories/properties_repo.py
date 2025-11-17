from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class PropertiesRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def create(self, name: str):
        obj = self.model(name=name)
        self.db.add(obj)

        try:
            self.db.commit()
            self.db.refresh(obj)
            return obj

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, propertie_id: int):
        return (
            self.db.query(self.model)
            .filter(self.model.id == propertie_id)
            .first()
        )

    def get_by_name(self, name: str):
        return (
            self.db.query(self.model).filter(self.model.name == name).first()
        )
