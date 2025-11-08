
# BookTrack API – Seu Skoob Pessoal com Análises Literárias

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento%20avançado-success?style=for-the-badge)


## Descrição

**BookTrack API** é uma aplicação backend desenvolvida em **FastAPI** para o gerenciamento e análise de uma biblioteca pessoal.  
O sistema permite cadastrar livros, acompanhar o progresso de leitura, importar coleções via **CSV** e gerar análises literárias por gênero, autor e status de leitura.  

Além de servir como ferramenta pessoal, o projeto oferece uma **view pública limitada**, possibilitando que terceiros explorem parte do acervo de forma segura.

A modelagem segue o padrão **Star Schema**, integrando conceitos de **engenharia de dados** e **boas práticas de APIs REST**.  
Este projeto foi idealizado como um estudo prático de **POO em Python**, **FastAPI**, **modelagem de dados** e **deploy em nuvem**.


## Diagrama ER – Modelo Estrela
```mermaid
erDiagram
    AUTORES {
        int id PK
        varchar nome
        varchar genero
        varchar pais_origem
    }
    EDITORAS {
        int id PK
        varchar nome
    }
    COLECOES {
        int id PK
        varchar nome
    }
    GENEROS {
        int id PK
        varchar nome
    }
    SUBGENEROS {
        int id PK
        varchar nome
        int genero_id FK
    }
    ESTANTES {
        int id PK
        varchar nome
    }
    FORMATOS {
        int id PK
        varchar nome
    }
    STATUS_LEITURA {
        int id PK
        varchar nome
    }
    ETIQUETAS {
        int id PK
        varchar nome
    }

    LIVROS {
        int id PK
        varchar titulo
        varchar isbn13
        int ano_publicacao
        int total_paginas
        varchar capa_url
        int editora_id FK
        int colecao_id FK
        int formato_id FK
    }

    LEITURAS {
        int id PK
        int livro_id FK
        int status_id FK
        date data_inicio
        date data_fim
        int paginas_lidas
        int avaliacao "1-5"
        text resenha
        boolean releitura
        varchar meta_pessoal
        date data_clube
        varchar clube_nome
        timestamp criado_em
        timestamp atualizado_em
    }

    LIVROS_AUTORES }o--o{ AUTORES : "escrito por"
    LIVROS_SUBGENEROS }o--o{ SUBGENEROS : "classificado como"
    LEITURAS_ETIQUETAS }o--o{ ETIQUETAS : "possui"
    LEITURAS_ESTANTES }o--o{ ESTANTES : "está na"

    LIVROS ||--o{ LEITURAS : "é lido em"
    LIVROS ||--o{ LIVROS_AUTORES : "tem"
    LIVROS ||--o{ LIVROS_SUBGENEROS : "tem"
    LEITURAS ||--o{ LEITURAS_ETIQUETAS : "tem"
    LEITURAS ||--o{ LEITURAS_ESTANTES : "está na"
    STATUS_LEITURA ||--o{ LEITURAS : "possui"
    EDITORAS ||--o{ LIVROS : "publica"
    COLECOES ||--o{ LIVROS : "contém"
    FORMATOS ||--o{ LIVROS : "tem formato"
    SUBGENEROS ||--o{ GENEROS : "pertence a"
```