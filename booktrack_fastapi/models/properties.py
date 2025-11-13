from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry_properties = registry()


@table_registry_properties.mapped_as_dataclass
class Properties:
    __abstract__ = True
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


@table_registry_properties.mapped_as_dataclass
class Publishers(Properties):
    __tablename__ = 'publishers'


@table_registry_properties.mapped_as_dataclass
class Formats(Properties):
    __tablename__ = 'formats'


@table_registry_properties.mapped_as_dataclass
class Collections(Properties):
    __tablename__ = 'collections'


@table_registry_properties.mapped_as_dataclass
class StatusReading(Properties):
    __tablename__ = 'reading_status'


@table_registry_properties.mapped_as_dataclass
class Tags(Properties):
    __tablename__ = 'tags'


@table_registry_properties.mapped_as_dataclass
class Shelves(Properties):
    __tablename__ = 'shelves'
