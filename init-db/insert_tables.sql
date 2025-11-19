INSERT INTO authors (id, name, gender, country_of_origin) VALUES
(1, 'Haruki Murakami', 'M', 'Japan'),
(2, 'Agatha Christie', 'F', 'United Kingdom'),
(3, 'George Orwell', 'M', 'United Kingdom'),
(4, 'Clarice Lispector', 'F', 'Brazil');


INSERT INTO publishers (id, name) VALUES
(1, 'Penguin Books'),
(2, 'HarperCollins'),
(3, 'Companhia das Letras');


INSERT INTO collections (id, name) VALUES
(1, 'Modern Classics'),
(2, 'Mystery Series'),
(3, 'Literatura Brasileira');


INSERT INTO shelves (id, name) VALUES
(1, 'Livros'),
(2, 'Revistas'),
(3, 'Artigos');


INSERT INTO formats (id, name) VALUES
(1, 'Físico'),
(2, 'E-book');


INSERT INTO reading_status (id, name) VALUES
(1, 'Lendo'),
(2, 'Concluído'),
(3, 'Abandonado');


INSERT INTO tags (id, name) VALUES
(1, 'Tenho'),
(2, 'Não Tendo');


INSERT INTO categories (id, name, parent_id) VALUES
(1, 'Ficção', NULL),
(2, 'Não-ficção', NULL),
(3, 'Fantasia', 1),
(4, 'Mistério', 1),
(5, 'Romance', 1),
(6, 'Distopia', 1),
(7, 'Biografia', 2);


INSERT INTO books (id, publisher_id, collection_id, format_id, category_id, author_id, title, 
                   original_publication_year, total_pages, cover_url)
VALUES
(1, 1, 1, 1, 6, 3, '1984', 1949, 328, 'https://covers.example.com/1984.jpg'),
(2, 1, 1, 1, 4, 2, 'Murder on the Orient Express', 1934, 256, 'https://covers.example.com/orient.jpg'),
(3, 3, 3, 1, 5, 4, 'A Hora da Estrela', 1977, 96, 'https://covers.example.com/hora.jpg'),
(4, 1, 1, 2, 5, 1, 'Norwegian Wood', 1987, 296, 'https://covers.example.com/wood.jpg');


INSERT INTO books_authors (book_id, author_id) VALUES
(1, 3),
(2, 2),
(3, 4),
(4, 1);


INSERT INTO books_categories (book_id, category_id) VALUES
(1, 6),  -- 1984 → Distopia
(2, 4),  -- Agatha → Mistério
(3, 5),  -- Clarice → Romance
(4, 5);  -- Murakami → Romance


INSERT INTO readings (id, book_id, status_id, start_date, end_date, pages_read,
                      personal_goal, club_date, club_name)
VALUES
(1, 1, 2, '2024-01-01', '2024-01-10', 328, NULL, NULL, NULL),
(2, 2, 1, '2024-03-05', NULL, 100, 'Ler até o fim do mês', NULL, NULL),
(3, 4, 2, '2023-11-01', '2023-11-20', 296, NULL, '2023-12-01', 'Clube do Livro XPTO');


INSERT INTO readings_tags (reading_id, tag_id) VALUES
(1, 1),  -- Distopia
(1, 4),  -- Clássico
(2, 2),  -- Suspense
(3, 3);  -- Reflexivo


INSERT INTO readings_shelves (reading_id, shelf_id) VALUES
(1, 1),  -- Lidos
(2, 3),  -- Favoritos (em leitura)
(3, 1),  -- Lidos
(3, 3);  -- Favoritos
