from typing import Optional

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: Optional[int] = None


class CategoriesList(BaseModel):
    data: list[Category]


class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryParentFilter(BaseModel):
    parent_id: Optional[int] = None
