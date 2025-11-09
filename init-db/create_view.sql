CREATE VIEW view_livros_leitura  AS SELECT
    l.titulo,
    a.nome AS autor,
	e.nome AS estante,
    COALESCE(grupo_pai.nome, 'Sem grupo') AS grupo,
    COALESCE(string_agg(c.nome, ' → '), 'Sem categoria') AS categorias,
    f.nome AS formato,
    s.nome AS status
FROM leituras lei
INNER JOIN livros l ON lei.livro_id = l.id
LEFT JOIN livros_autores la ON l.id = la.livro_id
LEFT JOIN autores a ON la.autor_id = a.id
INNER JOIN formatos f ON l.formato_id = f.id
INNER JOIN status_leitura s ON lei.status_id = s.id
INNER JOIN leituras_estantes le ON lei.id = le.leitura_id
INNER JOIN estantes e ON le.estante_id = e.id
LEFT JOIN livros_categorias lc ON l.id = lc.livro_id
LEFT JOIN categorias c ON lc.categoria_id = c.id
LEFT JOIN categorias sub ON c.pai_id = sub.id
LEFT JOIN categorias grupo_pai ON COALESCE(sub.pai_id, c.pai_id) = grupo_pai.id
GROUP BY 
    l.titulo, a.nome, grupo_pai.nome, f.nome, s.nome, e.nome;