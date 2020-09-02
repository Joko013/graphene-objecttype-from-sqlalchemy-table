=========================================
graphene-objecttype-from-sqlalchemy-table
=========================================


.. image:: https://img.shields.io/pypi/v/graphene_objecttype_from_sqlalchemy_table.svg
        :target: https://pypi.python.org/pypi/graphene_objecttype_from_sqlalchemy_table

.. image:: https://travis-ci.org/Joko013/graphene-objecttype-from-sqlalchemy-table.svg?branch=master
    :target: https://travis-ci.org/Joko013/graphene-objecttype-from-sqlalchemy-table



Transform SQLAlchemy_ ``Table`` into Graphene_ ``ObjectType``.


* Free software: MIT license

Features
--------

The purpose of this library is to allow a lightweight GraphQL schema creation based on database table definitions when full SQLAlchemy ORM cannot be used. It converts ``Table`` columns into their Graphene counterparts and creates the corresponding Graphene ``ObjectType`` to be used as a schema field.

Note that if your application uses SQLAlchemy ORM, `graphene-sqlalchemy`_ still offers more features and you could benefit from using it.


Installation
____________

In shell run:

.. code-block::

    pip install graphene-objecttype-from-sqlalchemy-table


Example usage
_____________

Let's start by defining a mock database table.

.. code-block:: python

    import sqlalchemy as sa

    t = sa.Table(
        'test_table',
        sa.MetaData(),
        sa.Column('foo', sa.String, doc='This will be passed to field description.'),
        sa.Column('bar', sa.Integer),
    )

Then create a Graphene object type using a Meta class with the reference to the SQLAlchemy table.

.. code-block:: python

    from graphene_objecttype_from_sqlalchemy_table import ObjectTypeFromTable

    class TestTable(ObjectTypeFromTable):
        class Meta:
            table = t

And finally define the GraphQL query structure using the new object type.

.. code-block:: python

    from graphene import Field, ObjectType, Schema

    class Query(ObjectType):
        test_table = Field(TestTable)

        # custom resolver for the table (probably a database query in a real world application)
        # returns a dictionary or an object with attributes corresponding to column names
        def resolve_test_table(root, info):
            return {'foo': 'Hello world', 'bar': 42}

    schema = Schema(query=Query)

    # confirm that the query resolves correctly
    schema.execute('query { testTable { foo, bar } }')
    # {'data': {'testTable': {'foo': 'Hello world', 'bar': 42}}}


It is possible to exclude specific columns from the resulting object by listing them as ``excluded_columns`` or to select only a subset of columns with ``only_selected_columns`` attribute.

.. code-block:: python

    class TestTable(ObjectTypeFromTable):
        class Meta:
            table = t
            excluded_columns = ('foo', )
            # only_selected_columns = ('bar', )

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _graphene-sqlalchemy: https://github.com/graphql-python/graphene-sqlalchemy
.. _Graphene: http://graphene-python.org/
.. _SQLAlchemy: http://www.sqlalchemy.org/
