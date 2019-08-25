import pytest
from mypackage import ExampleDatabase

@pytest.fixture
def db_connection():
    return ExampleDatabase('example_db')

def test_table_name(db_connection):
    assert db_connection.name == 'example_db'

def test_add_rows(db_connection):
    # DB should be empty
    assert db_connection.num_rows == 0
    # Try adding some data
    data = ['foo', 'bar', 'baz']
    db_connection.add_rows(data)
    # There should be 3 rows
    assert db_connection.num_rows == 3