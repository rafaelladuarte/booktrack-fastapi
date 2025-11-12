from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry_properties = registry()


@table_registry_properties.mapped_as_dataclass
class Properties:
    __abstract__ = True
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)


@table_registry_properties.mapped_as_dataclass
class Publishers(Properties):
    __tablename__ = 'editoras'


@table_registry_properties.mapped_as_dataclass
class Formats(Properties):
    __tablename__ = 'formatos'


@table_registry_properties.mapped_as_dataclass
class Collections(Properties):
    __tablename__ = 'colecoes'


@table_registry_properties.mapped_as_dataclass
class StatusReading(Properties):
    __tablename__ = 'status_leitura'


@table_registry_properties.mapped_as_dataclass
class Tags(Properties):
    __tablename__ = 'etiquetas'


@table_registry_properties.mapped_as_dataclass
class Shelves(Properties):
    __tablename__ = 'estantes'
