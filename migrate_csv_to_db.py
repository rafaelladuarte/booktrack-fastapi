from datetime import datetime

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

# Import application components
from booktrack_fastapi.core.database import engine
from booktrack_fastapi.models.authors import Authors
from booktrack_fastapi.models.books import Books
from booktrack_fastapi.models.categories import Categories
from booktrack_fastapi.models.collections import Collections
from booktrack_fastapi.models.formats import Formats
from booktrack_fastapi.models.publishers import Publishers
from booktrack_fastapi.models.reading_status import ReadingStatus
from booktrack_fastapi.models.readings import Readings
from booktrack_fastapi.models.shelves import Shelves
from booktrack_fastapi.models.tags import Tags

REPORT_FILE = "relatorio_antigravity.md"
CSV_FILE = "data/minha-biblioteca-leituras.csv"


def clean_val(val):
    if pd.isna(val) or val == "" or str(val).strip() == "-":
        return None
    return str(val).strip()


def parse_date(date_str):
    if not date_str:
        return None
    # Formats seen: 10/2025 (MM/YYYY)
    # Expected standard: DD/MM/YYYY or YYYY-MM-DD
    try:
        # Try DD/MM/YYYY
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        pass

    try:
        # Try MM/YYYY -> Default to 01/MM/YYYY
        return datetime.strptime(date_str, "%m/%Y").date()
    except ValueError:
        pass

    try:
        # Try YYYY
        return datetime.strptime(date_str, "%Y").date()
    except ValueError:
        pass

    return None


def get_or_create(session, model, **kwargs):
    stmt = select(model).filter_by(**kwargs)
    instance = session.scalar(stmt)
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.flush()
    return instance


def main():
    print("Iniciando migração...")

    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return

    report_lines = [
        "# Relatório Antigravity de Migração",
        "",
        "## Resumo de Erros",
        "",
        "| Linha | Erro | Detalhes | Sugestão |",
        "|-------|------|----------|----------|",
    ]

    errors_count = 0
    success_count = 0

    with Session(engine) as session:
        for index, row in df.iterrows():
            line_num = index + 2  # CSV header is line 1

            try:
                with session.begin_nested():
                    # 1. Parse Authors
                    author_name = clean_val(row.get('Escritor'))
                    if not author_name:
                        # Skip or create unknown?
                        # Assuming Author is required implies we need one.
                        # Books model: author_id is Mapped[int | None].
                        # So it handles None.
                        author = None
                    else:
                        # Extract extra author info
                        gender_raw = clean_val(row.get('GeneroEscritor'))
                        gender = None
                        if gender_raw:
                            if gender_raw.lower() in {'masculino', 'm'}:
                                gender = 'M'
                            elif gender_raw.lower() in {'feminino', 'f'}:
                                gender = 'F'

                        origin = clean_val(row.get('Origem'))

                        # Check existance by Name
                        author = session.scalar(
                            select(Authors).where(Authors.name == author_name)
                        )
                        if not author:
                            author = Authors(
                                name=author_name, gender=gender, country_of_origin=origin
                            )
                            session.add(author)
                            session.flush()

                    # 2. Publisher
                    publisher_name = clean_val(row.get('Editora'))
                    publisher = None
                    if publisher_name:
                        publisher = get_or_create(session, Publishers, name=publisher_name)

                    # 3. Format
                    format_name = clean_val(row.get('Formato'))
                    fmt = None
                    if format_name:
                        fmt = get_or_create(session, Formats, name=format_name)

                    # 4. Collection
                    collection_name = clean_val(row.get('Colecao'))
                    collection = None
                    if collection_name:
                        collection = get_or_create(session, Collections, name=collection_name)

                    # 5. Categories (Breadcrumb: Grupo -> Genero -> Subgenero)
                    # We link the book to the most specific one available.
                    group_name = clean_val(row.get('Grupo'))
                    genre_name = clean_val(row.get('Genero'))
                    subgenre_name = clean_val(row.get('Subgenero'))

                    final_category = None

                    if group_name:
                        group = get_or_create(
                            session, Categories, name=group_name, parent_id=None
                        )
                        final_category = group

                        if genre_name:
                            genre = get_or_create(
                                session, Categories, name=genre_name, parent_id=group.id
                            )
                            final_category = genre

                            if subgenre_name:
                                subgenre = get_or_create(
                                    session, Categories, name=subgenre_name, parent_id=genre.id
                                )
                                final_category = subgenre

                    # 6. Reading Status
                    status_name = clean_val(row.get('Status'))
                    if not status_name:
                        # Default to 'Não lido' or similar if missing?
                        # Or verify if nullable. Readings.status_id is ForeignKey,
                        # likely not nullable.
                        # Let's hope it's in the CSV or we fail row.
                        status_name = "Desconhecido"

                    status = get_or_create(
                        session, ReadingStatus, name=status_name
                    )

                    # 7. Book Identity
                    book_title = clean_val(row.get('Name'))
                    if not book_title:
                        raise ValueError("Título do livro (Name) está vazio.")

                    # Check for existing book
                    # We'll use Title + Author as unique identifier for this migration logic
                    stmt = select(Books).where(Books.title == book_title)
                    if author:
                        stmt = stmt.where(Books.author_id == author.id)

                    book = session.scalar(stmt)

                    if not book:
                        # Prepare fields
                        try:
                            if clean_val(row.get('AnoPublicacao')):
                                pub_year = int(row.get('AnoPublicacao'))
                            else:
                                pub_year = None
                        except Exception:
                            pub_year = None

                        try:
                            if clean_val(row.get('TotalPagina')):
                                pages = int(row.get('TotalPagina'))
                            else:
                                pages = None
                        except Exception:
                            pages = None

                        cover = clean_val(row.get('Capa'))

                        book = Books(
                            title=book_title,
                            original_publication_year=pub_year,
                            total_pages=pages,
                            cover_url=cover,
                            publisher_id=publisher.id if publisher else None,
                            collection_id=collection.id if collection else None,
                            format_id=fmt.id if fmt else None,
                            category_id=final_category.id if final_category else None,
                            author_id=author.id if author else None
                        )
                        session.add(book)
                        session.flush()

                        # Add M2M relationships (Authors, Categories)
                        if author and author not in book.authors:
                            book.authors.append(author)
                        if final_category and final_category not in book.categories:
                            book.categories.append(final_category)

                    # 8. Create Reading
                    # Check if reading exists for this book with this status?
                    # Or just add. A user might read a book multiple times.
                    # We will add a new reading entry.

                    start_date = parse_date(clean_val(row.get('DataInicio')))
                    end_date = parse_date(clean_val(row.get('DataFim')))
                    personal_goal = clean_val(row.get('Meta'))
                    club_name = clean_val(row.get('ClubeLivro'))
                    club_date = parse_date(clean_val(row.get('DataClube')))

                    reading = Readings(
                        book_id=book.id,
                        status_id=status.id,
                        start_date=start_date,
                        end_date=end_date,
                        personal_goal=personal_goal,
                        club_name=club_name,
                        club_date=club_date,
                        pages_read=None  # CSV doesn't specify progress, just total pages in Book
                    )
                    session.add(reading)
                    session.flush()

                    # 9. Shelves (Estante) - M2M
                    shelf_names = clean_val(row.get('Estante'))
                    if shelf_names:
                        # Assuming single value or comma separated?
                        # Sample "Livro"
                        # If comma separated:
                        for s_name in shelf_names.split(','):
                            s_new_name = s_name.strip()
                            if s_new_name:
                                shelf = get_or_create(session, Shelves, name=s_new_name)
                                reading.shelves.append(shelf)

                    # 10. Tags (Etiqueta) - M2M
                    # Sample "Tenho"
                    tag_names = clean_val(row.get('Etiqueta'))
                    if tag_names:
                        for t_name in tag_names.split(','):
                            t_new_name = t_name.strip()
                            if t_new_name:
                                tag = get_or_create(session, Tags, name=t_new_name)
                                reading.tags.append(tag)

                    success_count += 1

            except Exception as e:
                errors_count += 1
                error_msg = str(e)
                error_type = type(e).__name__
                # Basic suggestion logic
                suggestion = "Verificar dados da linha."
                if "IntegrityError" in error_type:
                    suggestion = "Violação de constraint (ex: duplicidade ou FK inexistente)."
                elif "ValueError" in error_type:
                    suggestion = "Formato de dados inválido (ex: data ou número)."

                report_lines.append(f"| {line_num} | {error_type} | {error_msg} | {suggestion} |")

        session.commit()

    # Write Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        for line in report_lines:
            f.write(line + "\n")

        f.write(f"\n\n**Resumo Final**:\n- Sucessos: {success_count}\n- Falhas: {errors_count}")

    print(f"Migração concluída. Sucessos: {success_count}, Falhas: {errors_count}")
    print(f"Relatório gerado em: {REPORT_FILE}")


if __name__ == "__main__":
    main()
