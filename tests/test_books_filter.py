from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.readings import Readings
from booktrack_fastapi.models.shelves import Shelves


@pytest.mark.asyncio
async def test_list_books_filter_shelve_id_success(
    async_client: AsyncClient,
    async_session: AsyncSession,
    auth_headers: dict,
):
    """Testa filtro por shelve_id que retorna livros corretamente."""
    # 1. Setup Data
    shelf1 = Shelves(name='Favoritos')
    shelf2 = Shelves(name='Lerei')
    status = ReadingStatus(name='Concluído')

    book1 = Books(title='Livro na Estante 1', original_publication_year=2021, total_pages=200)
    book2 = Books(title='Livro na Estante 2', original_publication_year=2022, total_pages=300)
    book3 = Books(title='Livro Sem Estante', original_publication_year=2023, total_pages=400)

    async_session.add_all([shelf1, shelf2, status, book1, book2, book3])
    await async_session.commit()
    await async_session.refresh(shelf1)
    await async_session.refresh(shelf2)
    await async_session.refresh(status)
    await async_session.refresh(book1)
    await async_session.refresh(book2)

    # Associar book1 à shelf1 via Reading
    reading1 = Readings(book_id=book1.id, status_id=status.id)
    reading1.shelves.append(shelf1)

    # Associar book2 à shelf2 via Reading
    reading2 = Readings(book_id=book2.id, status_id=status.id)
    reading2.shelves.append(shelf2)

    async_session.add_all([reading1, reading2])
    await async_session.commit()

    # 2. Test filter by shelf1
    response = await async_client.get(f'/books?shelve_id={shelf1.id}', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()['data']
    assert len(data) == 1
    assert data[0]['title'] == 'Livro na Estante 1'


@pytest.mark.asyncio
async def test_list_books_filter_shelve_id_nonexistent(
    async_client: AsyncClient,
    auth_headers: dict,
):
    """Testa filtro por shelve_id inexistente retorna lista vazia."""
    response = await async_client.get('/books?shelve_id=999', headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()['data']
    assert len(data) == 0


@pytest.mark.asyncio
async def test_list_books_no_filter(
    async_client: AsyncClient,
    async_session: AsyncSession,
    auth_headers: dict,
):
    """Testa listagem sem filtro retorna todos os livros."""
    book = Books(title='Livro Geral de Teste', original_publication_year=2020, total_pages=150)
    async_session.add(book)
    await async_session.commit()

    response = await async_client.get('/books', headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()['data']
    # Deve ter pelo menos o livro que acabamos de criar
    assert any(b['title'] == 'Livro Geral de Teste' for b in data)
