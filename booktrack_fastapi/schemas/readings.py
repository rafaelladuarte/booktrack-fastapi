from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from booktrack_fastapi.schemas.books import BookExpanded


class ReadingStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ReadingExpanded(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    pages_read: Optional[int] = None
    personal_goal: Optional[str] = None
    club_date: Optional[date] = None
    club_name: Optional[str] = None
    updated_at: Optional[datetime] = None
    review: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

    status: Optional[ReadingStatusSchema] = None

    # Nested Book Expanded Info
    book: Optional[BookExpanded] = None

    tags: list[str] = []
    shelves: list[str] = []

    @field_validator('tags', 'shelves', mode='before')
    @classmethod
    def convert_objects_to_names(cls, v):
        if isinstance(v, list):
            return [getattr(item, 'name', str(item)) for item in v]
        return v


class ReadingList(BaseModel):
    data: list[ReadingExpanded]


class ReadingQuery(BaseModel):
    status_id: Optional[int] = Field(None, description='Filtrar por ID do status')
    club_name: Optional[str] = Field(None, description='Filtrar pelo nome do Clube do Livro')


class ReadingUpdate(BaseModel):
    status_id: Optional[int] = Field(None, description='Atualizar id do status')
    club_name: Optional[str] = Field(None, description='Atualizar nome do Clube do Livro')
    pages_read: Optional[int] = Field(None, description='Atualizar número de páginas lidas')
    personal_goal: Optional[str] = Field(None, description='Atualizar objetivo pessoal')
    club_date: Optional[date] = Field(None, description='Atualizar data do Clube do Livro')
    start_date: Optional[date] = Field(None, description='Atualizar data de início')
    review: Optional[str] = Field(None, description='Atualizar resenha')
    rating: Optional[int] = Field(None, ge=1, le=5, description='Atualizar nota (1 a 5)')
    tag_ids: Optional[list[int]] = Field(None, description='Atualizar IDs das tags associadas')
    shelf_ids: Optional[list[int]] = Field(None, description='Atualizar IDs das estantes associadas')


class ReadingCreate(BaseModel):
    book_id: int
    status_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    pages_read: Optional[int] = None
    personal_goal: Optional[str] = None
    club_date: Optional[date] = None
    club_name: Optional[str] = None
    review: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
