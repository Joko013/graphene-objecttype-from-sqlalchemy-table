
from typing import Callable

from graphene.types.enum import Enum, EnumMeta
from sqlalchemy import types


enum_registry = dict()


def get_enum_from_sa_enum(sa_enum: types.Enum) -> EnumMeta:
    """Convert SQLAlchemy enum to Graphene enum."""
    name = sa_enum.name

    if name in enum_registry:
        # if the enum is reused for another field, use the existing graphene enum to avoid duplicate types
        enum = enum_registry[name]
    else:
        values = [(value, i) for i, value in enumerate(sa_enum.enums, start=1)]
        enum = Enum(name, values)
        enum_registry[name] = enum

    return enum


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
