from http import HTTPStatus
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse
)
def read_root_html():
    return """
        <html>
        <head>
            <title> Nosso olá mundo!</title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
        </html>
    """
