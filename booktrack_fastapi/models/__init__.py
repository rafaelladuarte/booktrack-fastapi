from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()

from booktrack_fastapi.models.authors import Authors
from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.categories import Categories
from booktrack_fastapi.models.properties import Properties
from booktrack_fastapi.models.reading import Readings

__all__ = ["Base", "Authors", "Books", "Categories", "Properties", "Readings"]