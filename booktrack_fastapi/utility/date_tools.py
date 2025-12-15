from datetime import datetime


def convert_str_to_date(item: dict) -> dict:
    """
    Converte campos de data de string (YYYY-MM-DD) para objetos date/datetime.
    Útil quando os dados vêm de uma fonte onde datas são strings e o Pydantic 
    ou SQLAlchemy espera objetos date.
    """
    date_fields = ['start_date', 'end_date', 'club_date', 'updated_at']

    for field in date_fields:
        if field in item and isinstance(item[field], str):
            try:
                # Tenta converter string YYYY-MM-DD para date
                # Ajuste o formato conforme necessário se suas strings forem diferentes
                item[field] = datetime.strptime(item[field], '%Y-%m-%d').date()
            except ValueError:
                # Se falhar (ex: formato incorreto), mantém o valor original ou loga erro
                pass
    return item
