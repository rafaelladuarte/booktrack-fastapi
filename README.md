
# BookTrack API – Gerenciamento de Livros com FastAPI 


[![Python](https://img.shields.io/badge/Python-3.13-yellow?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-3.9-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Alembic](https://img.shields.io/badge/Alembic-1.17.1-gray&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.44-red?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)




![alt text](docs/images/cover.png)

## Descrição

**BookTrack API** é uma aplicação backend desenvolvida em **FastAPI** para o gerenciamento e análise de uma biblioteca pessoal. O sistema permite cadastrar livros, acompanhar o progresso de leitura, importar coleções via **CSV** e gerar análises literárias por gênero, autor e status de leitura.  

Além de servir como ferramenta pessoal, o projeto oferece uma **view pública limitada**, possibilitando que terceiros explorem parte do acervo de forma segura.

A modelagem segue o padrão **Star Schema**, integrando conceitos de **engenharia de dados** e **boas práticas de APIs REST**. Este projeto foi idealizado como um estudo prático de **POO em Python**, **FastAPI**, **modelagem de dados** e **deploy em nuvem**.


## Diagrama ER – Modelo Estrela
```mermaid
erDiagram
    %% ========== 1. DIMENSÕES BÁSICAS ==========
    AUTORES {
        int id PK
        varchar nome
        varchar genero "M/F"
        varchar pais_origem
    }

    EDITORAS {
        int id PK
        varchar nome UK
    }

    COLECOES {
        int id PK
        varchar nome
    }

    ESTANTES {
        int id PK
        varchar nome UK
    }

    FORMATOS {
        int id PK
        varchar nome UK
    }

    STATUS_LEITURA {
        int id PK
        varchar nome UK
    }

    ETIQUETAS {
        int id PK
        varchar nome UK
    }

    %% ========== 2. CATEGORIAS HIERÁRQUICAS ==========
    CATEGORIAS {
        int id PK
        varchar nome
        int pai_id FK "NULL = categoria raiz"
    }

    %% ========== 3. LIVRO (com TODOS os campos corretos) ==========
    LIVROS {
        int id PK
        varchar titulo
        int ano_publicacao_original
        int total_paginas
        text capa_url
        int editora_id FK
        int colecao_id FK
        int formato_id FK
    }

    %% ========== 5. LEITURAS ==========
    LEITURAS {
        int id PK
        int livro_id FK
        int status_id FK
        date data_inicio
        date data_fim
        int paginas_lidas
        varchar meta_pessoal
        date data_clube
        varchar clube_nome
        timestamp criado_em
        timestamp atualizado_em
    }

    %% ========== RELACIONAMENTOS ==========
    %% Livro → Editoras (1:N)
    EDITORAS ||--o{ LIVROS : "publica"

    %% Livro → Coleções (1:N)
    COLECOES ||--o{ LIVROS : "contém"

    %% Livro → Formatos (1:N)
    FORMATOS ||--o{ LIVROS : "possui"

    %% Livro → Autores (N:N)
    LIVROS }o--o{ AUTORES : "escrito por"

    %% Livro → Categorias (N:N)
    LIVROS }o--o{ CATEGORIAS : "classificado em"

    %% Categorias hierárquicas (auto-relacionamento)
    CATEGORIAS }o--o{ CATEGORIAS : "subcategoria de"

    %% Leitura → Livro (N:1)
    LIVROS ||--o{ LEITURAS : "possui leituras"

    %% Leitura → Status (N:1)
    STATUS_LEITURA ||--o{ LEITURAS : "define"

    %% Leitura → Etiquetas (N:N)
    LEITURAS }o--o{ ETIQUETAS : "tem"

    %% Leitura → Estantes (N:N)
    LEITURAS }o--o{ ESTANTES : "está em"
```
