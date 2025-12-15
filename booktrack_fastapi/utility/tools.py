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
        # READING (For BookExpandedView context)
        'reading': {
            'id': row['reading_id'],
            'start_date': str(row['start_date']) if row.get('start_date') else None,
            'end_date': str(row['end_date']) if row.get('end_date') else None,
            'pages_read': row['pages_read'],
            'personal_goal': row['personal_goal'],
            'club_date': str(row['club_date']) if row.get('club_date') else None,
            'club_name': row['club_name'],
            'status': {
                'id': row['reading_status_id'],
                'name': row['reading_status_name'],
            }
            if row.get('reading_status_id')
            else None,
            'tags': (
                row['reading_tags'].split(', ') if row.get('reading_tags') else []
            ),
            'shelves': (
                row['reading_shelves'].split(', ')
                if row.get('reading_shelves')
                else []
            ),
        }
        if row.get('reading_id')
        else None,
    }


def expand_reading_row(row: dict) -> dict:
    """Expand fields for ReadingExpandedView response."""
    return {
        'id': row['reading_id'],
        'start_date': str(row['start_date']) if row.get('start_date') else None,
        'end_date': str(row['end_date']) if row.get('end_date') else None,
        'pages_read': row['pages_read'],
        'personal_goal': row['personal_goal'],
        'club_date': str(row['club_date']) if row.get('club_date') else None,
        'club_name': row['club_name'],
        'updated_at': str(row['updated_at']) if row.get('updated_at') else None,
        
        'status': {
            'id': row['status_id'],
            'name': row['status_name'],
        } if row.get('status_id') else None,
        
        'book': {
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
            } if row.get('author_id') else None,
            'publisher': {
                'id': row['publisher_id'],
                'name': row['publisher_name'],
            } if row.get('publisher_id') else None,
            'collection': {
                'id': row['collection_id'],
                'name': row['collection_name'],
            } if row.get('collection_id') else None,
            'format': {
                'id': row['format_id'],
                'name': row['format_name'],
            } if row.get('format_id') else None,
            'category': {
                'id': row['category_id'],
                'name': row['category_name'],
                'parent_id': row['category_parent_id'],
            } if row.get('category_id') else None,
        },
        
        'tags': row['reading_tags'].split(', ') if row.get('reading_tags') else [],
        'shelves': row['reading_shelves'].split(', ') if row.get('reading_shelves') else [],
    }


def convert_dates_to_str(item: dict) -> dict:
    """Converte datas para string e mapeia reading_id para id."""
    # Converter datas para string
    for key in ['start_date', 'end_date', 'updated_at', 'club_date']:
        val = item.get(key)
        if val is not None:
            item[key] = str(val)
    
    # Mapear reading_id para id (compatibilidade com schema)
    if 'reading_id' in item and 'id' not in item:
        item['id'] = item['reading_id']
    
    return item
