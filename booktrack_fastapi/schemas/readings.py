from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Reading(BaseModel):
    id: int
    book_id: int
    status_id: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    pages_read: Optional[int]
    personal_goal: Optional[str]
    club_date: Optional[str]
    club_name: Optional[str]
    reated_at: Optional[datetime]
    updated_at: Optional[datetime]


class ReadingList(BaseModel):
    data: list[Reading]


class ReadingQuery(BaseModel):
    status_id: Optional[str] = Field(None, description='Filtrar por ID do status')
    club_name: Optional[str] = Field(
        None, description='Filtrar pelo nome do Clube do Livro'
    )
