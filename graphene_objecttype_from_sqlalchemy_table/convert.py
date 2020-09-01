
from functools import singledispatch
from typing import Callable

from graphene import Field
from graphene.types import Boolean, Date, DateTime, Float, ID, Int, JSONString, Scalar, String
from graphene.types.enum import EnumMeta
from sqlalchemy import types, Column

from .enum import get_enum_from_sa_enum, get_enum_resolver


@singledispatch
def convert_column_type(type_, column: Column):
    """Based on SQLAlchemy column type return Graphene type.

    In case additional types need to be converted, the function can be patched, e.g.:
    ```
    from graphene_objecttype_from_sqlalchemy_table.convert import convert_column_type
    from graphene import String

    @convert_column_type.register(SomeCustomType)
    def _(type_, column):
        return String
    ```
    """
    raise TypeError(f"Don't know how to convert {column} of type {column.type.__class__}.")


@convert_column_type.register(types.String)
def _to_string_or_enum(type_, column):
    return String


@convert_column_type.register(types.Enum)
def _to_enum(type_, column):
    return get_enum_from_sa_enum(sa_enum=column.type)


@convert_column_type.register(types.DateTime)
def _to_datetime(type_, column):
    return DateTime


@convert_column_type.register(types.Date)
def _to_date(type_, column):
    return Date


@convert_column_type.register(types.SmallInteger)
@convert_column_type.register(types.Integer)
def _to_int(type_, column):
    return ID if column.primary_key else Int


@convert_column_type.register(types.Boolean)
def _to_boolean(type_, column):
    return Boolean


@convert_column_type.register(types.Float)
@convert_column_type.register(types.Numeric)
def _to_float(type_, column):
    return Float


@convert_column_type.register(types.JSON)
def _to_json_string(type_, column):
    return JSONString


def get_custom_resolver(field_type: Scalar, field_name: str) -> Callable:
    """Some field types require a custom resolver, create and return it, return `None` otherwise.

    For instance resolve enum strings to enum values.
    """
    if isinstance(field_type, EnumMeta):
        return get_enum_resolver(field_name=field_name, enum=field_type)


def convert_column(column: Column) -> Field:
    """Convert SQLAlchemy Column to corresponding Graphene Field."""
    field_type = convert_column_type(column.type, column)
    field_required = not column.nullable
    field_description = column.doc
    field_resolver = get_custom_resolver(field_type, column.name)

    return Field(type=field_type, required=field_required, description=field_description, resolver=field_resolver)
