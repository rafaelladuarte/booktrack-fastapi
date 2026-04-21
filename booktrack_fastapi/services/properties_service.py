from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class PropertiesService:
    def __init__(self, db: AsyncSession, model, repository_cls):
        self.db = db
        self.model = model
        self.repo = repository_cls(db, model)

    async def create(self, name: str, lenght: int = 2):
        """Cria um novo registro para uma entidade genérica (Editora, Formato, etc).

        Args:
            name: Nome do registro a ser criado.
            lenght: Comprimento mínimo exigido para o nome.

        Returns:
            True se criado com sucesso.

        Raises:
            HTTPException: 422 se o nome for muito curto.
            HTTPException: 409 se o registro com o mesmo nome já existir.
        """
        name = name.strip()

        if len(name) < lenght:
            raise HTTPException(
                status_code=422,
                detail=f'O nome deve ter pelo menos {lenght} caracteres.',
            )

        existing = await self.repo.get_by_name(name)
        if existing:
            raise HTTPException(
                status_code=409, detail=f"{self.model.__name__} '{name}' já existe."
            )

        await self.repo.create(name)

        return True

    async def list_all(self):
        """Lista todos os registros da entidade gerenciada.

        Returns:
            Lista de objetos do modelo.
        """
        return await self.repo.get_all()

    async def get_by_id(self, propertie_id: int):
        """Busca um registro específico da entidade pelo ID.

        Args:
            propertie_id: Identificador único do registro.

        Returns:
            O objeto encontrado.

        Raises:
            HTTPException: 404 se não for encontrado.
        """
        obj = await self.repo.get_by_id(propertie_id)

        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f'{self.model.__name__} id={propertie_id} não encontrado.',
            )

        return obj

    async def list_by_filter(self, **filters):
        """Lista registros aplicando filtros opcionais (atualmente não implementado).

        Args:
            **filters: Parâmetros de filtro.
        """
        # Assuming repo update didn't include filtered search, but keeping structure if needed
        pass
        # return await self.repo.get_filtered(**filters)
