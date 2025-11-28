from fastapi import FastAPI

from booktrack_fastapi.routers import (
    auth,
    authors,
    books,
    categories,
    properties,
    readings,
)

app = FastAPI(title='BookTrack API - Authentication Service')

# Rotas de autenticação (públicas)
app.include_router(auth.router)

# Rotas de recursos (protegidas)
app.include_router(properties.router)
app.include_router(categories.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(readings.router)
