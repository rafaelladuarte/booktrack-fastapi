CREATE OR REPLACE VIEW books_expanded_view AS
SELECT
    b.id AS book_id,
    b.title,
    b.original_publication_year,
    b.total_pages,
    b.cover_url,

    -- Autor principal (1:N na prática)
    a.id AS author_id,
    a.name AS author_name,
    a.gender AS author_gender,
    a.country_of_origin AS author_country,

    -- Publisher
    p.id AS publisher_id,
    p.name AS publisher_name,

    -- Collection
    c.id AS collection_id,
    c.name AS collection_name,

    -- Format
    f.id AS format_id,
    f.name AS format_name,

    -- Category
    cat.id AS category_id,
    cat.name AS category_name,
    cat.parent_id AS category_parent_id,

    -- Reading (pode ser null)
    r.id AS reading_id,
    r.start_date,
    r.end_date,
    r.pages_read,
    r.personal_goal,
    r.club_date,
    r.club_name,

    -- Reading Status
    rs.id AS reading_status_id,
    rs.name AS reading_status_name,

    -- Tags agregadas (pode ser string → depois você converte para array se quiser)
    (
        SELECT string_agg(t.name, ', ')
        FROM readings_tags rt
        JOIN tags t ON t.id = rt.tag_id
        WHERE rt.reading_id = r.id
    ) AS reading_tags,

    -- Shelves agregados
    (
        SELECT string_agg(s.name, ', ')
        FROM readings_shelves rs2
        JOIN shelves s ON s.id = rs2.shelf_id
        WHERE rs2.reading_id = r.id
    ) AS reading_shelves

FROM books b
LEFT JOIN books_authors ba ON ba.book_id = b.id
LEFT JOIN authors a ON a.id = ba.author_id

LEFT JOIN publishers p ON p.id = b.publisher_id
LEFT JOIN collections c ON c.id = b.collection_id
LEFT JOIN formats f ON f.id = b.format_id
LEFT JOIN categories cat ON cat.id = b.category_id

LEFT JOIN readings r ON r.book_id = b.id
LEFT JOIN reading_status rs ON rs.id = r.status_id;