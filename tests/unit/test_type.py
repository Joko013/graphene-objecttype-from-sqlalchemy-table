import pytest

from graphene import Field, String
from sqlalchemy import Column, types, Table, MetaData

from graphene_objecttype_from_sqlalchemy_table.type import ObjectTypeFromTable


def test_generate_fields(mocker):
    t = Table(
        'test_table',
        MetaData(),
        Column('foo', types.String),
        Column('bar', types.String),
    )

    field = Field(type=String)
    mocker.patch('graphene_objecttype_from_sqlalchemy_table.type.convert_column', return_value=field)
    assert ObjectTypeFromTable.generate_fields(
        table=t, excluded_columns=(), only_selected_columns=()
    ) == {'foo': field, 'bar': field}


@pytest.mark.parametrize(
    'excluded_columns, only_selected_columns, result',
    [
        ((), (), True),
        ((), ('foo', ), True),
        (('foo', ), (), False),
        ((), ('bar', ), False),
    ]
)
def test_column_should_be_converted(excluded_columns, only_selected_columns, result):
    assert ObjectTypeFromTable.column_should_be_converted('foo', excluded_columns, only_selected_columns) == result
