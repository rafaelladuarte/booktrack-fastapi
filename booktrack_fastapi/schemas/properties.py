from enum import Enum

from pydantic import BaseModel


class PropertyType(str, Enum):
    editoras = 'editoras'
    formatos = 'formatos'
    colecoes = 'colecoes'
    status_leitura = 'status_leitura'
    etiquetas = 'etiquetas'
    estantes = 'estantes'


class Property(BaseModel):
    id: int
    nome: str
