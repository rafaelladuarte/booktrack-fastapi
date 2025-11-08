-- ========== DIMENSÕES ==========
CREATE TABLE IF NOT EXISTS autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    genero VARCHAR(20),
    pais_origem VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS editoras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS colecoes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS generos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS subgeneros (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    genero_id INTEGER REFERENCES generos(id)
);

CREATE TABLE IF NOT EXISTS estantes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS formatos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS status_leitura (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS etiquetas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- ========== LIVROS ==========
CREATE TABLE IF NOT EXISTS livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    isbn13 VARCHAR(17),
    ano_publicacao INTEGER,
    total_paginas INTEGER,
    capa_url TEXT,
    editora_id INTEGER REFERENCES editoras(id),
    colecao_id INTEGER REFERENCES colecoes(id),
    formato_id INTEGER REFERENCES formatos(id)
);

-- ========== TABELA FATO ==========
CREATE TABLE IF NOT EXISTS leituras (
    id SERIAL PRIMARY KEY,
    livro_id INTEGER NOT NULL REFERENCES livros(id),
    status_id INTEGER NOT NULL REFERENCES status_leitura(id),
    data_inicio DATE,
    data_fim DATE,
    paginas_lidas INTEGER DEFAULT 0,
    meta_pessoal VARCHAR(300),
    data_clube DATE,
    clube_nome VARCHAR(200),
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

-- ========== JUNÇÕES ==========
CREATE TABLE IF NOT EXISTS livros_autores (
    livro_id INTEGER REFERENCES livros(id),
    autor_id INTEGER REFERENCES autores(id),
    PRIMARY KEY (livro_id, autor_id)
);

CREATE TABLE IF NOT EXISTS livros_subgeneros (
    livro_id INTEGER REFERENCES livros(id),
    subgenero_id INTEGER REFERENCES subgeneros(id),
    PRIMARY KEY (livro_id, subgenero_id)
);

CREATE TABLE IF NOT EXISTS leituras_etiquetas (
    leitura_id INTEGER REFERENCES leituras(id),
    etiqueta_id INTEGER REFERENCES etiquetas(id),
    PRIMARY KEY (leitura_id, etiqueta_id)
);

CREATE TABLE IF NOT EXISTS leituras_estantes (
    leitura_id INTEGER REFERENCES leituras(id),
    estante_id INTEGER REFERENCES estantes(id),
    PRIMARY KEY (leitura_id, estante_id)
);