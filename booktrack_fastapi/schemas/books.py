from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    original_publication_year: int
    total_pages: Optional[int] = None
    publisher_id: Optional[int] = None
    collection_id: Optional[int] = None
    format_id: Optional[int] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    cover_url: Optional[str]


class BookCreate(BaseModel):
    title: str
    original_publication_year: int
    total_pages: int
    publisher_id: Optional[int] = None
    collection_id: Optional[int] = None
    format_id: Optional[int] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    cover_url: Optional[str] = None


class BookList(BaseModel):
    data: list[Book]


class BookUpdate(BaseModel):
    publisher_id: Optional[int] = Field(None, description='Atualizar ID da editora')
    collection_id: Optional[int] = Field(None, description='Atualizar ID da coleção')
    format_id: Optional[int] = Field(None, description='Atualizar ID do formato')
    author_id: Optional[int] = Field(None, description='Atualizar ID do escritor')
    category_id: Optional[int] = Field(None, description='Atualizar ID da categoria')
    cover_url: Optional[str] = Field(None, description='Atualizar URL da capa')
    title: Optional[str] = Field(None, description='Atualizar título')
    original_publication_year: Optional[int] = Field(
        None, description='Atualizar ano de publicação original'
    )
    total_pages: Optional[int] = Field(None, description='Atualizar número total de páginas')


class BookFilter(BaseModel):
    title: Optional[str] = Field(None, description='Filtrar peli título completo do livro')
    year: Optional[int] = Field(None, description='FIltrar pelo ano de publicação original')
    publish_id: Optional[int] = Field(None, description='Filtrar por ID da editora')
    collection_id: Optional[int] = Field(None, description='Filtrar por ID da coleção')
    format_id: Optional[int] = Field(None, description='Filtrar por ID do formato')
    author_id: Optional[int] = Field(None, description='Filtrar por ID do escritor')
    author_name: Optional[str] = Field(None, description='Filtrar por parte do nome do autor')
    author_country: Optional[str] = Field(None, description='Filtrar pelo país de origem do autor')
    author_gender: Optional[str] = Field(None, description='Filtrar pelo gênero do autor')
    category_id: Optional[int] = Field(None, description='Filtrar por ID da categoria')
    shelve_id: Optional[int] = Field(None, description='Filtrar por ID da estante')
    tag_id: Optional[int] = Field(None, description='Filtrar por ID da tag (via leituras)')
    status_id: Optional[int] = Field(None, description='Filtrar por ID do status de leitura')


class AuthorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    gender: Optional[str] = None
    country_of_origin: Optional[str] = None


class PublisherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class CollectionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class FormatSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    parent_id: Optional[int] = None


class BookExpanded(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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


class BookExpandedList(BaseModel):
    data: list[BookExpanded]


class ReadingStatusSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ReadingSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    pages_read: Optional[int] = None
    status: Optional[ReadingStatusSimple] = None
    tags: list[str] = []
    shelves: list[str] = []
    
    @field_validator('tags', 'shelves', mode='before')
    @classmethod
    def validate_tags_shelves(cls, v):
        if isinstance(v, list):
            return [getattr(item, 'name', str(item)) for item in v]
        return v
    
    # Need to import field_validator for this, we'll do it cleanly without field_validator if possible,
    # or just add the import at the top. Let's add the import to the top of the file in another chunk.


class BookDetail(BookExpanded):
    readings: list[ReadingSimple] = []


class BookDetailList(BaseModel):
    data: list[BookDetail]
