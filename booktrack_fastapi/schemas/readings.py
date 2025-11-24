from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Reading(BaseModel):
    id: int
    book_id: int
    status_id: int
    start_date: Optional[str]
    end_date: Optional[str]
    pages_read: Optional[int]
    personal_goal: Optional[str]
    club_date: Optional[str] = Field(None, description='Data do Clube do Livro')
    club_name: Optional[str] = Field(None, description='Nome do Clube do Livro')
    updated_at: Optional[str]


class ReadingList(BaseModel):
    data: list[Reading]


class ReadingQuery(BaseModel):
    status_id: Optional[str] = Field(None, description='Filtrar por ID do status')
    club_name: Optional[str] = Field(
        None, description='Filtrar pelo nome do Clube do Livro'
    )


class ReadingUpdate(BaseModel):
    status_id: Optional[str] = Field(None, description='Atualizar id do status')
    club_name: Optional[str] = Field(
        None, description='Atualizar nome do Clube do Livro'
    )
    pages_read: Optional[int] = Field(None, description='Atualizar número de páginas lidas')
    personal_goal: Optional[str] = Field(None, description='Atualizar objetivo pessoal')
    club_date: Optional[str] = Field(None, description='Atualizar data do Clube do Livro')
    start_date: Optional[str] = Field(None, description='Atualizar data de início')
