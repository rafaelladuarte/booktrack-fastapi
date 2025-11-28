def item_to_dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


def expand_book_row(row: dict) -> dict:
    return {
        'id': row['book_id'],
        'title': row['title'],
        'original_publication_year': row['original_publication_year'],
        'total_pages': row['total_pages'],
        'cover_url': row['cover_url'],
        'author': {
            'id': row['author_id'],
            'name': row['author_name'],
            'gender': row['author_gender'],
            'country': row['author_country'],
        }
        if row.get('author_id')
        else None,
        'publisher': {
            'id': row['publisher_id'],
            'name': row['publisher_name'],
        }
        if row.get('publisher_id')
        else None,
        'collection': {
            'id': row['collection_id'],
            'name': row['collection_name'],
        }
        if row.get('collection_id')
        else None,
        'format': {
            'id': row['format_id'],
            'name': row['format_name'],
        }
        if row.get('format_id')
        else None,
        'category': {
            'id': row['category_id'],
            'name': row['category_name'],
            'parent_id': row['category_parent_id'],
        }
        if row.get('category_id')
        else None,
        # READING
        'reading': {
            'id': row['reading_id'],
            'start_date': row['start_date'],
            'end_date': row['end_date'],
            'pages_read': row['pages_read'],
            'personal_goal': row['personal_goal'],
            'club_date': row['club_date'],
            'club_name': row['club_name'],
            'status': {
                'id': row['reading_status_id'],
                'name': row['reading_status_name'],
            }
            if row.get('reading_status_id')
            else None,
            'tags': (
                row['reading_tags'].split(',') if row.get('reading_tags') else []
            ),
            'shelves': (
                row['reading_shelves'].split(',')
                if row.get('reading_shelves')
                else []
            ),
        }
        if row.get('reading_id')
        else None,
    }


def convert_dates(item: dict) -> dict:
    for key in ['start_date', 'end_date', 'updated_at', 'club_date']:
        val = item.get(key)
        if val is not None:
            item[key] = str(val)
    return item
