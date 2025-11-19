from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int
    title: str
    original_publication_year: int
    total_pages: Optional[int] = None
    publisher_id: Optional[int] = None
    collection_id: Optional[int] = None
    format_id: Optional[int] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    cover_url: Optional[str] = None


class BookCreate(BaseModel):
    title: str
    original_publication_year: int
    total_pages: int
    publisher_id: int | None = None
    collection_id: int | None = None
    format_id: int | None = None
    author_id: int | None = None
    category_id: int | None = None
    cover_url: str | None = None


class BookList(BaseModel):
    data: list[Book]


class BookUpdate(BaseModel):
    publish_id: Optional[int] = Field(None, description='Filtrar por ID da editora')
    collection_id: Optional[int] = Field(
        None, description='Filtrar por ID da coleção'
    )
    format_id: Optional[int] = Field(None, description='Filtrar por ID do formato')
    author_id: Optional[int] = Field(None, description='Filtrar por ID do escritor')
    category_id: Optional[int] = Field(
        None, description='Filtrar por ID da categoria'
    )
    shelve_id: Optional[int] = Field(None, description='Filtrar por ID da estante')


class BookFilter(BaseModel):
    title: Optional[str] = Field(
        None, description='Filtrar peli título completo do livro'
    )
    year: Optional[int] = Field(
        None, description='FIltrar pelo ano de publicação original'
    )
    publish_id: Optional[int] = Field(None, description='Filtrar por ID da editora')
    collection_id: Optional[int] = Field(
        None, description='Filtrar por ID da coleção'
    )
    format_id: Optional[int] = Field(None, description='Filtrar por ID do formato')
    author_id: Optional[int] = Field(None, description='Filtrar por ID do escritor')
    category_id: Optional[int] = Field(
        None, description='Filtrar por ID da categoria'
    )
    shelve_id: Optional[int] = Field(None, description='Filtrar por ID da estante')


class AuthorSchema(BaseModel):
    id: int
    name: str
    gender: Optional[str] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True


class PublisherSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CollectionSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FormatSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class BookExpanded(BaseModel):
    id: int
    title: str
    original_publication_year: Optional[int] = None
    total_pages: Optional[int] = None
    cover_url: Optional[str] = None

    author: Optional[AuthorSchema] = None
    publisher: Optional[PublisherSchema] = None
    collection: Optional[CollectionSchema] = None
    format: Optional[FormatSchema] = None
    category: Optional[CategorySchema] = None

    class Config:
        from_attributes = True


class BookExpandedList(BaseModel):
    data: list[BookExpanded]
