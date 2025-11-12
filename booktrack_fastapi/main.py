from http import HTTPStatus

from fastapi import FastAPI

from booktrack_fastapi.routers import properties, users

app = FastAPI(title='BookTrack API')


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


app.include_router(users.router)
app.include_router(properties.router)
