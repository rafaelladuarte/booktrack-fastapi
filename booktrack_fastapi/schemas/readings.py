from typing import Optional

from pydantic import BaseModel, Field

from booktrack_fastapi.schemas.books import BookExpanded


class ReadingStatusSchema(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class ReadingExpanded(BaseModel):
    id: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    pages_read: Optional[int] = None
    personal_goal: Optional[str] = None
    club_date: Optional[str] = None
    club_name: Optional[str] = None
    updated_at: Optional[str] = None
    
    status: Optional[ReadingStatusSchema] = None
    
    # Nested Book Expanded Info
    book: Optional[BookExpanded] = None
    
    tags: list[str] = []
    shelves: list[str] = []
    
    class Config:
        from_attributes = True


class ReadingList(BaseModel):
    data: list[ReadingExpanded]


class ReadingQuery(BaseModel):
    status_id: Optional[int] = Field(None, description='Filtrar por ID do status')
    club_name: Optional[str] = Field(
        None, description='Filtrar pelo nome do Clube do Livro'
    )


class ReadingUpdate(BaseModel):
    status_id: Optional[int] = Field(None, description='Atualizar id do status')
    club_name: Optional[str] = Field(
        None, description='Atualizar nome do Clube do Livro'
    )
    pages_read: Optional[int] = Field(
        None, description='Atualizar número de páginas lidas'
    )
    personal_goal: Optional[str] = Field(
        None, description='Atualizar objetivo pessoal'
    )
    club_date: Optional[str] = Field(
        None, description='Atualizar data do Clube do Livro'
    )
    start_date: Optional[str] = Field(None, description='Atualizar data de início')
