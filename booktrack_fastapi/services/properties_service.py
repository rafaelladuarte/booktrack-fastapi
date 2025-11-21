from fastapi import HTTPException
from sqlalchemy.orm import Session


class PropertiesService:
    def __init__(self, db: Session, model, repository_cls):
        self.db = db
        self.model = model
        self.repo = repository_cls(db, model)

    def create(self, name: str, lenght: int = 2):
        name = name.strip()

        if len(name) < lenght:
            raise HTTPException(
                status_code=422,
                detail=f'O nome deve ter pelo menos {lenght} caracteres.',
            )

        existing = self.repo.get_by_name(name)
        if existing:
            raise HTTPException(
                status_code=409, detail=f"{self.model.__name__} '{name}' já existe."
            )

        self.repo.create(name)

        return True

    def list_all(self):
        return self.repo.get_all()

    def get_by_id(self, propertie_id: int):
        obj = self.repo.get_by_id(propertie_id)

        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f'{self.model.__name__} id={propertie_id} não encontrado.',
            )

        return obj

    def list_by_filter(self, **filters):
        return self.repo.get_filtered(**filters)
