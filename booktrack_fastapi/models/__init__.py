# Association tables
from booktrack_fastapi.models.associations import (
    books_authors,
    books_categories,
    readings_shelves,
    readings_tags,
)

# Basic dimensions
from booktrack_fastapi.models.authors import Authors

# Main entities
from booktrack_fastapi.models.books import Books

# Hierarchical
from booktrack_fastapi.models.categories import Categories
from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.readings import Readings
from booktrack_fastapi.models.shelves import Shelves
from booktrack_fastapi.models.tags import Tags

from .base import Base

__all__ = [
    'Base',
    'books_authors',
    'books_categories',
    'readings_tags',
    'readings_shelves',
    'Authors',
    'Publishers',
    'Collections',
    'Shelves',
    'Formats',
    'ReadingStatus',
    'Tags',
    'Categories',
    'Books',
    'Readings',
]
