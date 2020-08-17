
from typing import Callable

from graphene.types.enum import Enum, EnumMeta
from sqlalchemy import Column


def is_enum(column: Column) -> bool:
    """Enums are interpreted as VARCHAR when used as Column types in a Table but have `enums` attribute."""
    enums = getattr(column.type, "enums", None)
    return bool(enums)


def get_enum_from_column(column: Column) -> EnumMeta:
    """Create Graphene Enum type from enumerated SQLAlchemy column."""
    name = column.type.name
    values = [(value, i) for i, value in enumerate(column.type.enums, start=1)]
    return Enum(name, values)


def get_enum_resolver(field_name: str, enum: EnumMeta) -> Callable:
    """Create a custom resolver for strings returned from queries to be returned as enums.

    Graphene expects enum class when checking the type of enum field value, but SQLAlchemy
    table.select() returns enums as strings.
    """

    def enum_resolver(parent, info):
        """Use the string value from the parent object to find the correct enum value and return it."""
        if isinstance(parent, dict):
            value = parent[field_name]
        else:
            value = getattr(parent, field_name)

        enum_value = getattr(enum, value) if isinstance(value, str) else value
        return enum_value

    return enum_resolver
