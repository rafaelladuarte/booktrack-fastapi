-- ========== 1. DIMENSÕES BÁSICAS ==========

-- Autores
CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    genero VARCHAR(1) CHECK (genero IN ('M', 'F')),
    pais_origem VARCHAR(100)
);

-- Editoras
CREATE TABLE editoras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL UNIQUE
);

-- Coleções (ex: Harry Potter, Fundação)
CREATE TABLE colecoes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL
);

-- Estantes (Literatura, Revistas, Acadêmico...)
CREATE TABLE estantes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Formatos do livro (Físico, eBook, Audiolivro)
CREATE TABLE formatos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Status da leitura (Lendo, Lido, Abandonado, Quero Ler, Pausado)
CREATE TABLE status_leitura (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Etiquetas rápidas (Tenho, Não Tenho, Emprestado, Desejado)
CREATE TABLE etiquetas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- ========== 2. CATEGORIAS FLEXÍVEIS ==========
-- Grupo -> Gênero → Subgênero → ...
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    pai_id INTEGER REFERENCES categorias(id),
    UNIQUE (pai_id, nome)
);

-- ========== 3. LIVROS ==========
CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    ano_publicacao_original INTEGER,
    total_paginas INTEGER,
    capa_url TEXT,
    editora_id INTEGER REFERENCES editoras(id),
    colecao_id INTEGER REFERENCES colecoes(id),
    formato_id INTEGER REFERENCES formatos(id)
);

-- ========== 4. JUNÇÕES ==========

-- Um livro pode ter vários autores
CREATE TABLE livros_autores (
    livro_id INTEGER REFERENCES livros(id) ON DELETE CASCADE,
    autor_id INTEGER REFERENCES autores(id) ON DELETE CASCADE,
    PRIMARY KEY (livro_id, autor_id)
);

-- Um livro pode ter várias categorias (Distopia + Cyberpunk + Ficção...)
CREATE TABLE livros_categorias (
    livro_id INTEGER REFERENCES livros(id) ON DELETE CASCADE,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (livro_id, categoria_id)
);

-- ========== 5. LEITURAS ==========
CREATE TABLE leituras (
    id SERIAL PRIMARY KEY,
    livro_id INTEGER NOT NULL REFERENCES livros(id) ON DELETE CASCADE,
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

-- Uma leitura pode ter várias etiquetas
CREATE TABLE leituras_etiquetas (
    leitura_id INTEGER REFERENCES leituras(id) ON DELETE CASCADE,
    etiqueta_id INTEGER REFERENCES etiquetas(id) ON DELETE CASCADE,
    PRIMARY KEY (leitura_id, etiqueta_id)
);

-- Uma leitura pode estar em várias estantes
CREATE TABLE leituras_estantes (
    leitura_id INTEGER REFERENCES leituras(id) ON DELETE CASCADE,
    estante_id INTEGER REFERENCES estantes(id) ON DELETE CASCADE,
    PRIMARY KEY (leitura_id, estante_id)
);