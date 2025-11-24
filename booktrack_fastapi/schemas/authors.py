from typing import Optional
from pydantic import BaseModel

class Author(BaseModel):
    id: int
    name: str
    gender: Optional[str] = None
    country_of_origin: Optional[str] = None

class AuthorCreate(BaseModel):
    name: str
    gender: Optional[str] = None
    country_of_origin: Optional[str] = None

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    country_of_origin: Optional[str] = None

class AuthorList(BaseModel):
    data: list[Author]
