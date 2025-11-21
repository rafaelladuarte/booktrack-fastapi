from fastapi import FastAPI

from booktrack_fastapi.routers import (
    authors,
    books,
    categories,
    properties,
    readings,
    users,
)

app = FastAPI(title='BookTrack API')

app.include_router(users.router)
app.include_router(properties.router)
app.include_router(categories.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(readings.router)
