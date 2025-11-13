
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


## Checklist de Desenvolvimento da API BookTrack

- [x] Planejar funcionalidades
- [x] Criar diagrama ER
- [ ] Implementar models SQLModel
- [ ] Criar rotas CRUD de Livros
- [ ] Escrever testes
- [ ] Configurar deploy no Render


## Diagrama ER – Modelo Estrela
```mermaid
erDiagram
    %% ========== 1. BASIC DIMENSIONS ==========
    AUTHORS {
        int id PK
        varchar name
        varchar gender "M/F"
        varchar country_of_origin
    }

    PUBLISHERS {
        int id PK
        varchar name UK
    }

    COLLECTIONS {
        int id PK
        varchar name
    }

    SHELVES {
        int id PK
        varchar name UK
    }

    FORMATS {
        int id PK
        varchar name UK
    }

    READING_STATUS {
        int id PK
        varchar name UK
    }

    TAGS {
        int id PK
        varchar name UK
    }

    %% ========== 2. HIERARCHICAL CATEGORIES ==========
    CATEGORIES {
        int id PK
        varchar name
        int parent_id FK "NULL = root category"
    }

    %% ========== 3. BOOKS ==========
    BOOKS {
        int id PK
        int publisher_id FK
        int collection_id FK
        int format_id FK
        int category_id FK 
        int authors FK
        varchar title
        int original_publication_year
        int total_pages
        text cover_url
        
    }

    %% ========== 5. READINGS ==========
    READINGS {
        int id PK
        int book_id FK
        int status_id FK
        date start_date
        date end_date
        int pages_read
        varchar personal_goal
        date club_date
        varchar club_name
        timestamp created_at
        timestamp updated_at
    }

    %% ========== RELATIONSHIPS ==========
    %% Book → Publishers (1:N)
    PUBLISHERS ||--o{ BOOKS : "publishes"

    %% Book → Collections (1:N)
    COLLECTIONS ||--o{ BOOKS : "contains"

    %% Book → Formats (1:N)
    FORMATS ||--o{ BOOKS : "has"

    %% Book → Authors (N:N)
    BOOKS }o--o{ AUTHORS : "written by"

    %% Book → Categories (N:N)
    BOOKS }o--o{ CATEGORIES : "classified as"

    %% Category → Category (self-relationship)
    CATEGORIES }o--o{ CATEGORIES : "sub-category of"

    %% Reading → Book (N:1)
    BOOKS ||--o{ READINGS : "has readings"

    %% Reading → ReadingStatus (N:1)
    READING_STATUS ||--o{ READINGS : "defines"

    %% Reading → Tags (N:N)
    READINGS }o--o{ TAGS : "tagged with"

    %% Reading → Shelves (N:N)
    READINGS }o--o{ SHELVES : "stored in"
```
