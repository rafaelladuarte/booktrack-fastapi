from enum import Enum

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class PropertyList(BaseModel):
    data: list[Property]


class PropertyTypeCreate(str, Enum):
    publishers = 'publishers'
    collections = 'collections'
    tags = 'tags'


class PropertyCreate(BaseModel):
    name: str
