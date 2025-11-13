from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int
    title: str
    original_publication_year: int
    total_pages: Optional[int] = None
    publish: Optional[str] = None
    collection: Optional[str] = None
    format: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[str] = None


class BookList(BaseModel):
    books: list[Book]


class BookQuery(BaseModel):
    title: Optional[str] = Field(
        None, description='Título parcial ou completo do livro'
    )
    year: Optional[int] = Field(None, description='Ano de publicação original')
    publish_id: Optional[int] = Field(
        None, description='Filtrar por ID da editora'
    )
    collection_id: Optional[int] = Field(
        None, description='Filtrar por ID da coleção'
    )
    format_id: Optional[int] = Field(
        None, description='Filtrar por ID do formato'
    )
    author_id: Optional[int] = Field(
        None, description='Filtrar por ID do escritor'
    )
    category_id: Optional[int] = Field(
        None, description='Filtrar por ID da categoria'
    )
