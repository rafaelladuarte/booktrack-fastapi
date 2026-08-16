import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from booktrack_fastapi.models import *
from booktrack_fastapi.models.reading_quotes import ReadingQuotes

async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:////home/elladarte/Documentos/my_github/booktrack-app/booktrack-backend/data/booktrack.db")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    from booktrack_fastapi.services.books_service import BooksService
    from booktrack_fastapi.schemas.books import BookCreate

    async with async_session() as db:
        service = BooksService(db)
        data = BookCreate(
            title="Livro de Teste 123",
            original_publication_year=2021,
            total_pages=200,
            synopsis="Test synopsis"
        )
        try:
            book = await service.create(data)
            print("Book created:", book.id)
        except Exception as e:
            print("Error:", e)

asyncio.run(test_db())
