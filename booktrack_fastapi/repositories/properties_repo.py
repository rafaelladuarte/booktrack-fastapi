from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PropertiesRepository:
    def __init__(self, db: AsyncSession, model):
        self.db = db
        self.model = model

    async def create(self, name: str):
        """Cria um novo registro para o modelo genérico associado.

        Args:
            name: Valor do campo 'name'.

        Returns:
            O objeto criado e persistido.
        """
        obj = self.model(name=name)
        self.db.add(obj)

        try:
            await self.db.commit()
            await self.db.refresh(obj)
            return obj

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_all(self):
        """Lista todos os registros da tabela vinculada ao modelo.

        Returns:
            Lista de instâncias do modelo.
        """
        stmt = select(self.model)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, propertie_id: int):
        """Busca um registro por ID na tabela do modelo.

        Args:
            propertie_id: ID primário.

        Returns:
            O objeto encontrado ou None.
        """
        stmt = select(self.model).where(self.model.id == propertie_id)
        result = await self.db.scalars(stmt)
        return result.first()
        # Alternative: return await self.db.get(self.model, propertie_id)

    async def get_by_name(self, name: str):
        """Busca um registro pelo campo nome exato (case-insensitive).

        Args:
            name: Nome a ser pesquisado.

        Returns:
            O objeto encontrado ou None.
        """
        stmt = select(self.model).where(self.model.name.ilike(name))
        result = await self.db.scalars(stmt)
        return result.first()
