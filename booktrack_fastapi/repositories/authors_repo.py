from sqlalchemy import delete, select, update

from booktrack_fastapi.core.dependencies import SessionDep
from booktrack_fastapi.models.authors import Authors


class AuthorsRepository:
    def __init__(self, db: SessionDep):
        self.db = db

    async def get_all(self):
        """Lista todos os autores cadastrados.

        Returns:
            Lista de instâncias de Authors.
        """
        stmt = select(Authors)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(self, author_id: int):
        """Busca um autor pelo seu identificador único.

        Args:
            author_id: ID do autor.

        Returns:
            Objeto Authors ou None.
        """
        return await self.db.get(Authors, author_id)

    async def create(self, parameters: dict):
        """Persiste um novo autor no banco de dados.

        Args:
            parameters: Atributos do autor.

        Returns:
            Instância de Authors criada.
        """
        item = Authors(**parameters)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_by_id(self, author_id: int, parameters: dict):
        """Atualiza os dados de um autor existente por ID.

        Args:
            author_id: ID do autor.
            parameters: Dicionário com campos a serem atualizados.

        Returns:
            O autor atualizado.
        """
        stmt = update(Authors).where(Authors.id == author_id).values(**parameters)
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_by_id(author_id)

    async def delete_by_id(self, author_id: int):
        """Remove um autor do banco de dados por ID.

        Args:
            author_id: ID do autor a ser removido.
        """
        stmt = delete(Authors).where(Authors.id == author_id)
        await self.db.execute(stmt)
        await self.db.commit()
