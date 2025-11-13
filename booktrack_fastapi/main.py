from fastapi import FastAPI

from booktrack_fastapi.routers import books, categories, properties, readings

app = FastAPI(title='BookTrack API')

app.include_router(properties.router)
app.include_router(categories.router)
app.include_router(books.router)
app.include_router(readings.router)
