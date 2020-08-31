
import pytest
from graphene.types.enum import Enum, EnumMeta
from sqlalchemy import types

from graphene_objecttype_from_sqlalchemy_table.enum import get_enum_from_sa_enum, get_enum_resolver, enum_registry


def test_get_enum_from_sa_enum():
    enum = types.Enum('foo', 'bar', name='test_enum')
    result = get_enum_from_sa_enum(sa_enum=enum)
    result_ = get_enum_from_sa_enum(sa_enum=enum)
    assert (
        isinstance(result, EnumMeta) and
        all(getattr(result, e, None) is not None for e in enum.enums) and
        result is result_ is enum_registry[enum.name]  # test that duplicate types are not being created
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
