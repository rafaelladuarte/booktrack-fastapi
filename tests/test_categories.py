# ruff: noqa: PLR2004
from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.categories import Categories


async def test_list_categories_no_filter(
    async_client: AsyncClient, async_session: AsyncSession, auth_headers: dict
):
    """
    Garante que buscar sem filtros traga todas as categorias cadastradas no banco.
    """
    parent = Categories(name='Global_Category')
    async_session.add(parent)
    await async_session.commit()
    await async_session.refresh(parent)

    child = Categories(name='Local_Category', parent_id=parent.id)
    async_session.add(child)
    await async_session.commit()

    response = await async_client.get('/categories', headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()['data']
    assert len(data) >= 2


async def test_list_categories_filter_parent_id(
    async_client: AsyncClient, async_session: AsyncSession, auth_headers: dict
):
    """
    Cobre o caso de filtro via `parent_id`, retornando
    apenas categorias filhas do parent determinado.
    """
    parent1 = Categories(name='Parent_A')
    parent2 = Categories(name='Parent_B')
    async_session.add_all([parent1, parent2])
    await async_session.commit()
    await async_session.refresh(parent1)
    await async_session.refresh(parent2)

    child1 = Categories(name='Child_A', parent_id=parent1.id)
    child2 = Categories(name='Child_B', parent_id=parent2.id)
    async_session.add_all([child1, child2])
    await async_session.commit()

    response = await async_client.get(f'/categories?parent_id={parent1.id}', headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()['data']

    assert len(data) == 1
    assert data[0]['name'] == 'Child_A'
    assert data[0]['parent_id'] == parent1.id


async def test_list_categories_filter_nonexistent_parent_id(
    async_client: AsyncClient, auth_headers: dict
):
    """
    Espera retorno de array vazia na data via payload JSON
    se parent_id não tiver filhos informados.
    """
    response = await async_client.get('/categories?parent_id=99999', headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'data': []}
