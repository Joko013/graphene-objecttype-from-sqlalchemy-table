#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "graphene>=2.1.3,<3",
    "sqlalchemy>=1.2,<2",
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', "pytest-mock==3.3.0" ]

setup(
    author="Jan Klima",
    author_email='klima013@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Transform SQLAlchemy Table into Graphene ObjectType.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='graphene_objecttype_from_sqlalchemy_table',
    name='graphene_objecttype_from_sqlalchemy_table',
    packages=find_packages(include=['graphene_objecttype_from_sqlalchemy_table', 'graphene_objecttype_from_sqlalchemy_table.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Joko013/graphene-objecttype-from-sqlalchemy-table',
    version='0.1.2',
    zip_safe=False,
)
