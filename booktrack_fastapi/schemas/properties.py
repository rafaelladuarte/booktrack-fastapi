from enum import Enum

from pydantic import BaseModel, Field


class PropertyType(str, Enum):
    publishers = 'publishers'
    formats = 'formats'
    collections = 'collections'
    reading_status = 'reading_status'
    tags = 'tags'
    shelves = 'shelves'


class Property(BaseModel):
    id: int
    name: str


class PropertyList(BaseModel):
    properties: list[Property]


class PropertyTypeCreate(str, Enum):
    publishers = 'publishers'
    collections = 'collections'
    tags = 'tags'


class PropertyCreate(BaseModel):
    name: str = Field(..., example='Sci-fi')
