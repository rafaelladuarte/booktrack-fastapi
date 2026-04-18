from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.categories import Categories


class CategoriesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        """Retorna todas as categorias sem filtros.

        Returns:
            Lista de objetos Categories.
        """
        stmt = select(Categories)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, category_id: int):
        """Busca uma categoria pelo ID primário.

        Args:
            category_id: ID da categoria.

        Returns:
            Objeto Categories ou None.
        """
        return await self.db.get(Categories, category_id)

    async def get_by_parent_id(self, parent_id: int):
        """Busca categorias que possuem um determinado pai.

        Args:
            parent_id: ID da categoria pai.

        Returns:
            Lista de categorias filhas.
        """
        stmt = select(Categories).where(Categories.parent_id == parent_id)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_filtered(self, **filters):
        """Busca categorias aplicando filtros opcionais.

        Args:
            **filters: Parâmetros de filtro flexíveis (ex: parent_id).

        Returns:
            Lista de categorias que atendem aos filtros definidos.
        """
        stmt = select(Categories)
        conditions = []
        if 'parent_id' in filters:
            conditions.append(Categories.parent_id == filters['parent_id'])

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_name_and_parent(self, name: str, parent_id: int = None):
        """Verifica se já existe uma categoria com o mesmo nome sob o mesmo pai.

        Args:
            name: Nome da categoria.
            parent_id: ID do pai (opcional).

        Returns:
            Objeto encontrado ou lista vazia.
        """
        stmt = select(Categories).where(Categories.parent_id == parent_id, Categories.name == name)
        result = await self.db.scalars(stmt)
        return result.all()

    async def create(self, name: str, parent_id: int | None = None):
        """Persiste uma nova categoria na hierarquia.

        Args:
            name: Nome da categoria.
            parent_id: ID do pai (se houver).

        Returns:
            Instância de Categories criada.
        """
        item = Categories(name=name, parent_id=parent_id)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item
