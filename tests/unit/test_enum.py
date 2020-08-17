
import pytest
from graphene.types.enum import Enum, EnumMeta
from sqlalchemy import types, Column

from graphene_objecttype_from_sqlalchemy_table.enum import is_enum, get_enum_from_column, get_enum_resolver


@pytest.mark.parametrize(
    'col_type, result',
    [
        (types.Enum('foo', 'bar', name='test_enum'), True),
        (types.String, False),
    ]
)
def test_is_enum(col_type, result):
    column = Column(name='test', type_=col_type)
    assert is_enum(column) == result


def test_get_enum_from_column():
    enum = types.Enum('foo', 'bar', name='test_enum')
    column = Column('test', enum)
    result = get_enum_from_column(column)
    assert (
        isinstance(result, EnumMeta) and
        all(getattr(result, e, None) is not None for e in enum.enums)
    )


class MockParentData:
    def __init__(self, value):
        self.test = value


@pytest.mark.parametrize(
    'parent',
    [
        ({"test": "one"}),
        (MockParentData("one")),
    ]
)
def test_enum_resolver_string(parent):
    """Resolve strings to enum values."""
    enum = Enum("test", [("one", 1), ("two", 2)])
    resolve = get_enum_resolver("test", enum)
    assert resolve(parent, None) == enum.one


def test_enum_resolver_non_string():
    """Resolve other data types to themselves."""
    parent = MockParentData(123)
    enum = Enum("test", [("one", 1), ("two", 2)])
    resolve = get_enum_resolver("test", enum)
    assert resolve(parent, None) is parent.test
