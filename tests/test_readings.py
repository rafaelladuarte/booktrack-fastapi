# ruff: noqa: PLR6301, PLR2004
from http import HTTPStatus

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.readings import Readings


class TestReadingsRoutes:
    """Suite de testes para as rotas de Readings."""

    async def test_list_readings_empty(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """
        Test GET /readings - Deve retornar lista vazia quando não há leituras.
        """
        response = await async_client.get('/readings', headers=auth_headers)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'data': []}

    async def test_list_readings_with_data(
        self,
        async_client: AsyncClient,
        async_session: AsyncSession,
        auth_headers: dict,
    ):
        """
        Test GET /readings - Deve retornar lista com dados após inserção.
        """
        # Arrange: Criar dados de teste
        status = ReadingStatus(name='Lendo')
        async_session.add(status)
        await async_session.commit()
        await async_session.refresh(status)

        book = Books(
            title='Test Book for Reading',
            original_publication_year=2024,
            total_pages=300,
        )
        async_session.add(book)
        await async_session.commit()
        await async_session.refresh(book)

        reading = Readings(
            book_id=book.id,
            status_id=status.id,
            pages_read=150,
            personal_goal='Terminar até o fim do mês',
        )
        async_session.add(reading)
        await async_session.commit()

        # Act: Fazer requisição
        response = await async_client.get('/readings', headers=auth_headers)

        # Assert: Verificar resposta
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert 'data' in data
        assert len(data['data']) == 1

        # Verificar estrutura aninhada
        assert data['data'][0]['book']['id'] == book.id
        assert data['data'][0]['status']['id'] == status.id
        assert data['data'][0]['pages_read'] == 150

    async def test_update_reading_success(
        self,
        async_client: AsyncClient,
        async_session: AsyncSession,
        auth_headers: dict,
    ):
        """
        Test PUT /readings/{book_id} - Deve atualizar uma leitura existente.
        """
        status = ReadingStatus(name='Em Progresso')
        async_session.add(status)
        await async_session.commit()
        await async_session.refresh(status)

        book = Books(
            title='Book to Update Reading',
            original_publication_year=2023,
            total_pages=400,
        )
        async_session.add(book)
        await async_session.commit()
        await async_session.refresh(book)

        reading = Readings(
            book_id=book.id,
            status_id=status.id,
            pages_read=100,
        )
        async_session.add(reading)
        await async_session.commit()

        # Act: Atualizar a leitura
        update_data = {
            'pages_read': 250,
            'personal_goal': 'Ler 50 páginas por dia',
        }
        response = await async_client.put(
            f'/readings/{book.id}', json=update_data, headers=auth_headers
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'detail': 'Reading updated successfully!'}

        await async_session.refresh(reading)
        assert reading.pages_read == 250
        assert reading.personal_goal == 'Ler 50 páginas por dia'

    async def test_update_reading_not_found(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """
        Test PUT /readings/{book_id} - Deve retornar 404 para book_id inexistente.
        """
        update_data = {'pages_read': 100}
        response = await async_client.put(
            '/readings/99999', json=update_data, headers=auth_headers
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_list_readings_with_filter(
        self,
        async_client: AsyncClient,
        async_session: AsyncSession,
        auth_headers: dict,
    ):
        """
        Test GET /readings?status_id=X - Deve filtrar leituras por status.
        """
        status_reading = ReadingStatus(name='Lendo')
        status_finished = ReadingStatus(name='Finalizado')
        async_session.add_all([status_reading, status_finished])
        await async_session.commit()
        await async_session.refresh(status_reading)
        await async_session.refresh(status_finished)

        book1 = Books(title='Book 1', original_publication_year=2024, total_pages=200)
        book2 = Books(title='Book 2', original_publication_year=2024, total_pages=300)
        async_session.add_all([book1, book2])
        await async_session.commit()
        await async_session.refresh(book1)
        await async_session.refresh(book2)

        reading1 = Readings(book_id=book1.id, status_id=status_reading.id)
        reading2 = Readings(book_id=book2.id, status_id=status_finished.id)
        async_session.add_all([reading1, reading2])
        await async_session.commit()

        # Act: Filtrar por status "Lendo"
        response = await async_client.get(
            f'/readings?status_id={status_reading.id}', headers=auth_headers
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data['data']) == 1
        assert data['data'][0]['status']['id'] == status_reading.id
