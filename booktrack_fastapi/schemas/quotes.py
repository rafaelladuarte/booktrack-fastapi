from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class QuoteSchema(BaseModel):
    """Serialização de uma citação de leitura."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    reading_id: int
    content: str
    page_number: Optional[int] = None
    created_at: Optional[datetime] = None


class QuoteCreate(BaseModel):
    """Payload para criação de uma nova citação ou nota de leitura."""

    content: str = Field(..., min_length=1, description='Texto da citação ou nota pessoal')
    page_number: Optional[int] = Field(None, ge=1, description='Número da página (opcional)')


class QuoteList(BaseModel):
    data: list[QuoteSchema]
