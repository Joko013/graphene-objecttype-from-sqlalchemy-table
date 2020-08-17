
from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from sqlalchemy import Table

from .convert import convert_column


class ObjectTypeFromTableOptions(ObjectTypeOptions):
    table = None


class ObjectTypeFromTable(ObjectType):
    @classmethod
    def __init_subclass_with_meta__(
        cls,
        table: Table = None,
        excluded_columns: tuple = (),
        only_selected_columns: tuple = (),
        **options
    ):
        if not isinstance(table, Table):
            raise TypeError(f"Attribute 'table' is {table.__class__} instead of {Table}.")

        if excluded_columns and only_selected_columns:
            raise ValueError("Use either `excluded_columns` or `only_selected_columns` but not both.")

        _meta = ObjectTypeFromTableOptions(cls)

        _meta.table = table
        _meta.fields = cls.generate_fields(
            table=table,
            excluded_columns=excluded_columns,
            only_selected_columns=only_selected_columns
        )

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def generate_fields(cls, table: Table, excluded_columns: tuple, only_selected_columns: tuple) -> dict:
        """Create mapping of Graphene Fields from Table columns."""

        fields = {
            c.name: convert_column(column=c) for c in table.columns
            if cls.column_should_be_converted(c.name, excluded_columns, only_selected_columns)
        }
        return fields

    @staticmethod
    def column_should_be_converted(column_name: str, excluded_columns: tuple, only_selected_columns: tuple) -> bool:
        """A column should be converted if it isn't excluded or is one of the selected columns, if they exist."""
        return column_name not in excluded_columns \
            and (not only_selected_columns or column_name in only_selected_columns)
