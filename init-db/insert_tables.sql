-- 1. AUTORES (5)
INSERT INTO autores (nome, genero, pais_origem) VALUES
('Clarice Lispector', 'F', 'Ucrânia'),
('George Orwell', 'M', 'Reino Unido'),
('J.K. Rowling', 'F', 'Reino Unido'),
('Yuval Noah Harari', 'M', 'Israel'),
('Agatha Christie', 'F', 'Reino Unido');

-- 2. EDITORAS (4)
INSERT INTO editoras (nome) VALUES
('Rocco'),
('Companhia das Letras'),
('Intrínseca'),
('HarperCollins Brasil');

-- 3. COLEÇÕES (4)
INSERT INTO colecoes (nome) VALUES
('Harry Potter'),
('As Crônicas de Gelo e Fogo'),
('Duna'),
('O Senhor dos Anéis');

-- 4. FORMATOS (5)
INSERT INTO formatos (nome) VALUES
('Físico'),
('eBook'),
('Audiolivro');

-- 5. STATUS DE LEITURA (5)
INSERT INTO status_leitura (nome) VALUES
('Lendo'),
('Concluído'),
('Abandonado'),
('Quero Ler'),
('Pausado');

-- 6. ESTANTES (5)
INSERT INTO estantes (nome) VALUES
('Livro'),
('Revistas')
('Artigos');


-- 7. ETIQUETAS (5)
INSERT INTO etiquetas (nome) VALUES
('Tenho'),
('Não Tenho'),
('Emprestado');


-- 8. CATEGORIAS
INSERT INTO categorias (nome, pai_id) VALUES
-- Raiz
('Ficção', NULL),
('Não-Ficção', NULL),

-- Nível 1
('Distopia', 1),
('Fantasia', 1),
('História', 2),

-- Nível 2
('Cyberpunk', 3),
('Grimdark', 4);

-- 9. LIVROS (5)
INSERT INTO livros (titulo, ano_publicacao_original, total_paginas, capa_url, editora_id, colecao_id, formato_id) VALUES
('1984', 1949, 336, 'https://example.com/1984.jpg', 2, NULL, 2),
('Harry Potter e a Pedra Filosofal',  1997, 320, 'https://example.com/hp1.jpg', 1, 1, 1),
('Sapiens',  2015, 448, 'https://example.com/sapiens.jpg', 2, NULL, 3),
('Neuromancer',  1984, 368, 'https://example.com/neuromancer.jpg', 1, NULL, 2),
('O Hobbit',  1937, 312, 'https://example.com/hobbit.jpg', 4, 4, 1);

-- 10. LIVROS x AUTORES
INSERT INTO livros_autores (livro_id, autor_id) VALUES
(1,2),  -- 1984 → Orwell
(2,3),  -- Harry Potter → Rowling
(3,4);  -- Sapiens → Harari

-- 11. LIVROS x CATEGORIAS
INSERT INTO livros_categorias (livro_id, categoria_id) VALUES
(1, 3), (1, 6),           -- 1984 = Distopia + Cyberpunk
(2, 4), (2, 7),           -- Harry Potter = Fantasia + Grimdark
(3, 5),                   -- Sapiens = História
(4, 3), (4, 6),   		  -- Neuromancer = Distopia + Cyberpunk
(5, 4);                   -- O Hobbit = Fantasia

-- 12. LEITURAS (5)
INSERT INTO leituras (livro_id, status_id, data_inicio, data_fim, paginas_lidas, meta_pessoal, data_clube, clube_nome) VALUES
(1, 2, '2025-01-10', '2025-01-15', 336, 'Terminar antes do clube', '2025-01-20', 'Clube Distopia'),
(2, 1, '2025-03-01', NULL, 150, 'Ler 1 capítulo por dia', NULL, NULL),
(3, 2, '2025-02-05', '2025-02-28', 448, 'Entender história humana', NULL, NULL),
(4, 4, NULL, NULL, 0, 'Comprar edição física primeiro', '2025-06-10', 'Clube Cyberpunk'),
(5, 1, '2025-04-01', NULL, 80, 'Ler antes de dormir', NULL, NULL);

-- 13. LEITURAS x ETIQUETAS
INSERT INTO leituras_etiquetas (leitura_id, etiqueta_id) VALUES
(1,1), (1,3),  -- 1984: tenho + emprestado
(2,2);         -- Harry Potter: não tenho

-- 14. LEITURAS x ESTANTES
INSERT INTO leituras_estantes (leitura_id, estante_id) VALUES
(1,1),  -- 1984 → Livros
(2,1),  -- Harry Potter → Livros
(3,3),  -- Sapiens → Artigos
(4,2),  -- Neuromancer → Revistas
(5,1);  -- O Hobbit → Livros