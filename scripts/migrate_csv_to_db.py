# ruff: noqa
"""Script de importação do CSV para o banco PostgreSQL.

Executa de forma assíncrona usando AsyncSession.
É idempotente: pode ser executado mais de uma vez com segurança.

Uso:
    python migrate_csv_to_db.py
"""

import asyncio
import logging
from datetime import date, datetime

import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.core.database import async_session_maker
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
from booktrack_fastapi.models.associations import readings_tags, readings_shelves

# ---------------------------------------------------------------------------
# Constantes de normalização
# ---------------------------------------------------------------------------

CSV_FILE = 'data/minha-biblioteca-leituras.csv'

# Correções de nomes de autores com variações no CSV
AUTHOR_CORRECTIONS: dict[str, str] = {
    'Jeff Vandermeer': 'Jeff VanderMeer',
}

# Normalização de case para Status e Etiqueta
CASE_CORRECTIONS: dict[str, str] = {
    'Em análise': 'Em Análise',
}

# Mapeamento do gênero do escritor (CSV → model String(1))
GENDER_MAP: dict[str, str] = {
    'Feminino': 'F',
    'Masculino': 'M',
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def clean_val(val) -> str | None:
    """Retorna None para valores vazios, NaN ou '-'; str limpa caso contrário."""
    if val is None:
        return None
    if isinstance(val, float) and pd.isna(val):
        return None
    s = str(val).strip()
    if s in ('', '-', 'nan'):
        return None
    return s


def parse_date_ddmmyyyy(value: str | None) -> date | None:
    """Converte string DD/MM/YYYY para date. Retorna None em caso de erro."""
    if not value:
        return None
    try:
        return datetime.strptime(value, '%d/%m/%Y').date()
    except ValueError:
        logger.warning('  ⚠ Data inválida (DD/MM/YYYY): "%s" — ignorada', value)
        return None


def parse_date_mmyyyy(value: str | None) -> date | None:
    """Converte string MM/YYYY para date(YYYY, MM, 1). Retorna None em caso de erro."""
    if not value:
        return None
    try:
        dt = datetime.strptime(value, '%m/%Y')
        return date(dt.year, dt.month, 1)
    except ValueError:
        logger.warning('  ⚠ Data inválida (MM/YYYY): "%s" — ignorada', value)
        return None


def normalize(value: str | None, corrections: dict[str, str]) -> str | None:
    """Aplica mapa de correções ao valor, se existir."""
    if value is None:
        return None
    return corrections.get(value, value)


# ---------------------------------------------------------------------------
# get_or_create com cache em memória
# ---------------------------------------------------------------------------


async def get_or_create_simple(
    session: AsyncSession,
    model,
    cache: dict,
    cache_key: str,
    name: str,
) -> object:
    """Busca entidade no cache local ou cria no banco se não existir.

    Usado para entidades com campo único `name` (Publishers, Formats, etc.).
    """
    if cache_key in cache:
        return cache[cache_key]

    instance = await session.scalar(select(model).where(model.name == name))
    if not instance:
        instance = model(name=name)
        session.add(instance)
        await session.flush()

    cache[cache_key] = instance
    return instance


async def get_or_create_category(
    session: AsyncSession,
    cache: dict,
    cache_key: str,
    name: str,
    parent_id: int | None,
) -> Categories:
    """Busca categoria no cache ou cria no banco.

    Usa name + parent_id para evitar colisão entre categorias homônimas
    em níveis hierárquicos diferentes.
    """
    if cache_key in cache:
        return cache[cache_key]

    instance = await session.scalar(
        select(Categories).where(
            Categories.name == name,
            Categories.parent_id == parent_id,
        )
    )
    if not instance:
        instance = Categories(name=name, parent_id=parent_id)
        session.add(instance)
        await session.flush()

    cache[cache_key] = instance
    return instance


# ---------------------------------------------------------------------------
# Etapa 1 — Entidades simples
# ---------------------------------------------------------------------------


async def importar_entidades_simples(
    session: AsyncSession,
    df: pd.DataFrame,
    cache: dict,
) -> None:
    """Importa Authors, Publishers, Collections, Formats, ReadingStatus, Shelves e Tags."""
    print('Importando entidades simples...')

    authors_count = 0
    publishers_count = 0
    collections_count = 0
    formats_count = 0
    status_count = 0
    shelves_count = 0
    tags_count = 0
    status_normalizado: list[str] = []

    for _, row in df.iterrows():
        # --- Authors ---
        author_name_raw = clean_val(row.get('Escritor'))
        if author_name_raw:
            # Aplicar correções de nome antes do get_or_create
            author_name = AUTHOR_CORRECTIONS.get(author_name_raw, author_name_raw)
            cache_key = f'Author:{author_name}'

            if cache_key not in cache:
                gender_raw = clean_val(row.get('GeneroEscritor'))
                gender = GENDER_MAP.get(gender_raw) if gender_raw else None
                origin = clean_val(row.get('Origem'))

                instance = await session.scalar(select(Authors).where(Authors.name == author_name))
                if not instance:
                    instance = Authors(
                        name=author_name,
                        gender=gender,
                        country_of_origin=origin,
                    )
                    session.add(instance)
                    await session.flush()
                    authors_count += 1

                cache[cache_key] = instance

        # --- Publishers ---
        pub_name = clean_val(row.get('Editora'))
        if pub_name:
            key = f'Publisher:{pub_name}'
            if key not in cache:
                await get_or_create_simple(session, Publishers, cache, key, pub_name)
                publishers_count += 1

        # --- Collections ---
        col_name = clean_val(row.get('Colecao'))
        if col_name:
            key = f'Collection:{col_name}'
            if key not in cache:
                await get_or_create_simple(session, Collections, cache, key, col_name)
                collections_count += 1

        # --- Formats ---
        fmt_name = clean_val(row.get('Formato'))
        if fmt_name:
            key = f'Format:{fmt_name}'
            if key not in cache:
                await get_or_create_simple(session, Formats, cache, key, fmt_name)
                formats_count += 1

        # --- ReadingStatus ---
        status_raw = clean_val(row.get('Status'))
        # Tratar None e '-' como "Quero Ler" (decisão aprovada)
        if not status_raw:
            status_raw = 'Quero Ler'
            title = clean_val(row.get('Name'))
            if title and title not in status_normalizado:
                status_normalizado.append(title)
        status_name = normalize(status_raw, CASE_CORRECTIONS)
        key = f'Status:{status_name}'
        if key not in cache:
            await get_or_create_simple(session, ReadingStatus, cache, key, status_name)
            status_count += 1

        # --- Shelves ---
        shelf_name = clean_val(row.get('Estante'))
        if shelf_name:
            key = f'Shelf:{shelf_name}'
            if key not in cache:
                await get_or_create_simple(session, Shelves, cache, key, shelf_name)
                shelves_count += 1

        # --- Tags (Etiqueta) ---
        tag_raw = clean_val(row.get('Etiqueta'))
        if tag_raw:
            tag_name = normalize(tag_raw, CASE_CORRECTIONS)
            key = f'Tag:{tag_name}'
            if key not in cache:
                await get_or_create_simple(session, Tags, cache, key, tag_name)
                tags_count += 1

    print(f'  ✓ Authors: {authors_count} criados')
    print(f'  ✓ Publishers: {publishers_count} criados')
    print(f'  ✓ Collections: {collections_count} criados')
    print(f'  ✓ Formats: {formats_count} criados')
    print(f'  ✓ ReadingStatus: {status_count} criados')
    print(f'  ✓ Shelves: {shelves_count} criados')
    print(f'  ✓ Tags: {tags_count} criados')
    if status_normalizado:
        print(
            f'  ⚠ {len(status_normalizado)} status normalizados para "Quero Ler": {status_normalizado}'
        )


# ---------------------------------------------------------------------------
# Etapa 2 — Categorias
# ---------------------------------------------------------------------------


async def importar_categorias(
    session: AsyncSession,
    df: pd.DataFrame,
    cache: dict,
) -> None:
    """Importa Categories em hierarquia: Grupo → Genero → Subgenero."""
    print('Importando categorias...')

    grupos_count = 0
    generos_count = 0
    subgeneros_count = 0

    # Passagem 1: Grupos (parent_id=None)
    for _, row in df.iterrows():
        grupo_name = clean_val(row.get('Grupo'))
        if not grupo_name:
            continue
        key = f'Cat:Grupo:{grupo_name}'
        if key not in cache:
            await get_or_create_category(session, cache, key, grupo_name, parent_id=None)
            grupos_count += 1

    # Passagem 2: Gêneros (parent_id=grupo.id)
    for _, row in df.iterrows():
        grupo_name = clean_val(row.get('Grupo'))
        genero_name = clean_val(row.get('Genero'))
        if not grupo_name or not genero_name:
            continue

        grupo = cache.get(f'Cat:Grupo:{grupo_name}')
        if not grupo:
            continue

        key = f'Cat:Genero:{genero_name}'
        if key not in cache:
            await get_or_create_category(session, cache, key, genero_name, parent_id=grupo.id)
            generos_count += 1

    # Passagem 3: Subgêneros (parent_id=genero.id)
    for _, row in df.iterrows():
        genero_name = clean_val(row.get('Genero'))
        subgenero_name = clean_val(row.get('Subgenero'))
        if not genero_name or not subgenero_name:
            continue

        genero = cache.get(f'Cat:Genero:{genero_name}')
        if not genero:
            continue

        key = f'Cat:Subgenero:{subgenero_name}'
        if key not in cache:
            await get_or_create_category(session, cache, key, subgenero_name, parent_id=genero.id)
            subgeneros_count += 1

    print(f'  ✓ Grupos: {grupos_count}')
    print(f'  ✓ Gêneros: {generos_count}')
    print(f'  ✓ Subgêneros: {subgeneros_count}')


# ---------------------------------------------------------------------------
# Etapa 3 — Livros
# ---------------------------------------------------------------------------


async def importar_livros(
    session: AsyncSession,
    df: pd.DataFrame,
    cache: dict,
) -> None:
    """Importa Books com todos os relacionamentos de FKs."""
    print('Importando livros...')

    livros_count = 0
    livros_pulados = 0

    for _, row in df.iterrows():
        title = clean_val(row.get('Name'))
        if not title:
            continue

        book_key = f'Book:{title}'

        # Idempotência: verificar se livro já existe no banco
        existing = await session.scalar(select(Books).where(Books.title == title))
        if existing:
            cache[book_key] = existing
            livros_pulados += 1
            continue

        # Author
        author_name_raw = clean_val(row.get('Escritor'))
        author = None
        if author_name_raw:
            author_name = AUTHOR_CORRECTIONS.get(author_name_raw, author_name_raw)
            author = cache.get(f'Author:{author_name}')

        # Publisher
        pub_name = clean_val(row.get('Editora'))
        publisher = cache.get(f'Publisher:{pub_name}') if pub_name else None

        # Collection
        col_name = clean_val(row.get('Colecao'))
        collection = cache.get(f'Collection:{col_name}') if col_name else None

        # Format
        fmt_name = clean_val(row.get('Formato'))
        fmt = cache.get(f'Format:{fmt_name}') if fmt_name else None

        # Category — mais específica disponível
        subgenero_name = clean_val(row.get('Subgenero'))
        genero_name = clean_val(row.get('Genero'))
        grupo_name = clean_val(row.get('Grupo'))

        category = None
        if subgenero_name and f'Cat:Subgenero:{subgenero_name}' in cache:
            category = cache[f'Cat:Subgenero:{subgenero_name}']
        elif genero_name and f'Cat:Genero:{genero_name}' in cache:
            category = cache[f'Cat:Genero:{genero_name}']
        elif grupo_name and f'Cat:Grupo:{grupo_name}' in cache:
            category = cache[f'Cat:Grupo:{grupo_name}']

        # AnoPublicacao
        try:
            ano_raw = clean_val(row.get('AnoPublicacao'))
            pub_year = int(float(ano_raw)) if ano_raw else None
        except (ValueError, TypeError):
            pub_year = None

        # TotalPagina
        try:
            pages_raw = clean_val(row.get('TotalPagina'))
            total_pages = int(float(pages_raw)) if pages_raw else None
        except (ValueError, TypeError):
            total_pages = None

        # Capa
        cover_url = clean_val(row.get('Capa'))

        book = Books(
            title=title,
            original_publication_year=pub_year,
            total_pages=total_pages,
            cover_url=cover_url,
            author_id=author.id if author else None,
            publisher_id=publisher.id if publisher else None,
            collection_id=collection.id if collection else None,
            format_id=fmt.id if fmt else None,
            category_id=category.id if category else None,
        )
        session.add(book)
        await session.flush()

        cache[book_key] = book
        livros_count += 1

    print(f'  ✓ {livros_count} livros criados')
    if livros_pulados:
        print(f'  ↩ {livros_pulados} livros já existiam (pulados)')


# ---------------------------------------------------------------------------
# Etapa 4 — Leituras
# ---------------------------------------------------------------------------


async def importar_leituras(
    session: AsyncSession,
    df: pd.DataFrame,
    cache: dict,
) -> None:
    """Importa Readings com M2M de Tags e Shelves."""
    print('Importando leituras...')

    leituras_count = 0
    leituras_puladas = 0

    for _, row in df.iterrows():
        title = clean_val(row.get('Name'))
        if not title:
            continue

        book = cache.get(f'Book:{title}')
        if not book:
            logger.warning('  ⚠ Livro não encontrado no cache: "%s" — leitura ignorada', title)
            continue

        # Idempotência: verificar se já existe reading para esse book_id
        existing_reading = await session.scalar(select(Readings).where(Readings.book_id == book.id))
        if existing_reading:
            leituras_puladas += 1
            continue

        # ReadingStatus
        status_raw = clean_val(row.get('Status'))
        if not status_raw:
            status_raw = 'Quero Ler'
        status_name = normalize(status_raw, CASE_CORRECTIONS)
        status = cache.get(f'Status:{status_name}')
        if not status:
            # Fallback para "Quero Ler" se status não encontrado no cache
            status = cache.get('Status:Quero Ler')

        # Datas
        start_date = parse_date_ddmmyyyy(clean_val(row.get('DataInicio')))
        end_date = parse_date_ddmmyyyy(clean_val(row.get('DataFim')))
        club_date = parse_date_mmyyyy(clean_val(row.get('DataClube')))

        # Outros campos
        personal_goal = clean_val(row.get('Meta'))
        club_name = clean_val(row.get('ClubeLivro'))

        reading = Readings(
            book_id=book.id,
            status_id=status.id,
            start_date=start_date,
            end_date=end_date,
            personal_goal=personal_goal,
            club_name=club_name,
            club_date=club_date,
            pages_read=None,
        )
        session.add(reading)
        await session.flush()

        # M2M: Tags (Etiqueta) — INSERT direto na tabela de associação
        # Usar Core insert() para evitar MissingGreenlet em contexto async
        tag_raw = clean_val(row.get('Etiqueta'))
        if tag_raw:
            tag_name = normalize(tag_raw, CASE_CORRECTIONS)
            tag = cache.get(f'Tag:{tag_name}')
            if tag:
                await session.execute(
                    insert(readings_tags).values(reading_id=reading.id, tag_id=tag.id)
                )

        # M2M: Shelves (Estante) — INSERT direto na tabela de associação
        shelf_name = clean_val(row.get('Estante'))
        if shelf_name:
            shelf = cache.get(f'Shelf:{shelf_name}')
            if shelf:
                await session.execute(
                    insert(readings_shelves).values(reading_id=reading.id, shelf_id=shelf.id)
                )

        leituras_count += 1

    print(f'  ✓ {leituras_count} leituras criadas')
    if leituras_puladas:
        print(f'  ↩ {leituras_puladas} leituras já existiam (puladas)')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> None:
    """Ponto de entrada do script de importação."""
    print('Lendo CSV...')
    df = pd.read_csv(CSV_FILE)

    # Remover linha completamente vazia (última linha do CSV)
    df = df.dropna(subset=['Name'])
    # Garantir que '-' e strings vazias não-NaN sejam tratados no clean_val
    df = df.where(pd.notna(df), None)

    print(f'  {len(df)} linhas de dados encontradas\n')

    async with async_session_maker() as session:
        cache: dict = {}

        await importar_entidades_simples(session, df, cache)
        print()
        await importar_categorias(session, df, cache)
        print()
        await importar_livros(session, df, cache)
        print()
        await importar_leituras(session, df, cache)
        print()

        # Commit único ao final
        await session.commit()

    print('Importação concluída com sucesso.')


if __name__ == '__main__':
    asyncio.run(main())
