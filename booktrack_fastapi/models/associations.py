from sqlalchemy import Column, ForeignKey, Table

from .base import Base

# BOOKS ↔ AUTHORS
books_authors = Table(
    'books_authors',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True),
)

# BOOKS ↔ CATEGORIES
books_categories = Table(
    'books_categories',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
)

# READINGS ↔ TAGS
readings_tags = Table(
    'readings_tags',
    Base.metadata,
    Column('reading_id', ForeignKey('readings.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)

# READINGS ↔ SHELVES
readings_shelves = Table(
    'readings_shelves',
    Base.metadata,
    Column('reading_id', ForeignKey('readings.id'), primary_key=True),
    Column('shelf_id', ForeignKey('shelves.id'), primary_key=True),
)
