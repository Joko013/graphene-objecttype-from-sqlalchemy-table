
import pytest

from graphene import Boolean, Date, DateTime, Enum, Float, ID, Int, JSONString, String
from sqlalchemy import types, Column

from graphene_objecttype_from_sqlalchemy_table.convert import convert_column_type, get_custom_resolver


@pytest.mark.parametrize(
    'type_, result',
    [
        (types.NVARCHAR, String),
        (types.VARCHAR, String),
        (types.TEXT, String),
        (types.NUMERIC, Float),
        (types.BIGINT, Int),
        (types.SMALLINT, Int),
        (types.DATETIME, DateTime),
        (types.DATE, Date),
        (types.BOOLEAN, Boolean),
        (types.JSON, JSONString),
    ]
)
def test_convert_type(type_, result):
    column = Column('test', type_)
    assert convert_column_type(column.type, column) == result


def test_convert_type_primary_key():
    column = Column('test', types.Integer, primary_key=True)
    assert convert_column_type(column.type, column) == ID


def test_convert_type_enum(mocker):
    graphene_enum = Enum("test", [("one", 1), ("two", 2)])
    mocker.patch("graphene_objecttype_from_sqlalchemy_table.convert.get_enum_from_sa_enum", return_value=graphene_enum)

    enum = types.Enum("one", "two", name="test_enum")
    column = Column('test', enum)
    assert convert_column_type(column.type, column) == graphene_enum


mock_function = lambda _: None


@pytest.mark.parametrize(
    'field_type, result',
    [
        (String, None),
        (Enum("test", [("one", 1), ("two", 2)]), mock_function),
    ]
)
def test_get_custom_resolver(mocker, field_type, result):
    mocker.patch("graphene_objecttype_from_sqlalchemy_table.convert.get_enum_resolver", return_value=mock_function)
    assert get_custom_resolver(field_type, "test") == result
