from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from booktrack_fastapi.routers import (
    auth,
    authors,
    books,
    categories,
    properties,
    readings,
)

app = FastAPI(title='BookTrack API - Authentication Service')


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"detail": "Recurso não encontrado"})


# Rotas de autenticação (públicas)
app.include_router(auth.router)

# Rotas de recursos (protegidas)
app.include_router(properties.router)
app.include_router(categories.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(readings.router)
