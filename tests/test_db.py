import pytest
import sqlite3
from unittest.mock import Mock
from unittest.mock import patch

from pathlib import Path
from inflammation.db import connect_to_database, query_database


@pytest.fixture(scope="session")
def database_fn_fixture(tmp_path_factory):
    return tmp_path_factory.mktemp("data") / "test.db"

@pytest.fixture(scope="session")
def database_connection(database_fn_fixture):
    """
    Create database connection
    """
    conn = sqlite3.connect(database_fn_fixture)
    yield conn
    conn.close()
    Path.unlink(database_fn_fixture)

def test_query_database_mock(database_fn_fixture):
    """Mock the query_database function to show the principle
    """
    sql = "SELECT * FROM Animals"
    conn = connect_to_database(database_fn_fixture)
    query_database = Mock()
    query_database.return_value = ("Jerry", "Mouse", 1)
    assert query_database(sql, connection=conn) == ("Jerry", "Mouse", 1)
    query_database.assert_called_once_with(sql, connection=conn)

class MockResponse:
    @staticmethod
    def connection():
        return {"mock_key": "mock_response"}
    
def test_query_db_mocked_connection(monkeypatch):
    """Mock the database connection and cursor to ensure the correct methods
    are called within the query_database function
    """

    # Create a mock sqlite3.Connection object
    mock_conn = Mock()

    # Create a mock sqlite3.Cursor object
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [("Jerry", "Mouse", 1)]
    mock_conn.cursor.return_value = mock_cursor

    # with patch('sqlite3.connect') as mock_connection:
    def get_mock_connection(*args, **kwargs):
        return mock_conn

    monkeypatch.setattr(sqlite3, "connect",  get_mock_connection)
    conn = sqlite3.connect("my_non_existent_file")
    mock_cursor = conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [("Jerry", "Mouse", 1)]
    # make our fake connection
    conn = conn("my_non_existent_file")
    sql = "SELECT * FROM Animals"
    # test what query_database does with our fake connection
    result = query_database(sql, conn=conn)
    assert result[0] == ("Jerry", "Mouse", 1)
    # check that query_database passes our SQL string to cursor.execute()
    mock_cursor.execute.assert_called_once_with(sql)
    # check that fetchall() was called
    mock_cursor.fetchall.assert_called_once()
    # check that query_database closes the connection
    conn.close.assert_called_once()

@patch("sqlite3.connect")
def test_query_db_mocked_connection(mock_connection):
    """Mock the database connection and cursor to ensure the correct methods
    are called within the query_database function
    """
    mock_cursor = mock_connection.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [("Jerry", "Mouse", 1)]
    # make our fake connection
    conn = mock_connection("my_non_existent_file")
    sql = "SELECT * FROM Animals"
    # test what query_database does with our fake connection
    result = query_database(sql, conn=conn)
    assert result[0] == ("Jerry", "Mouse", 1)
    # check that query_database passes our SQL string to cursor.execute()
    mock_cursor.execute.assert_called_once_with(sql)
    # check that fetchall() was called
    mock_cursor.fetchall.assert_called_once()
    # check that query_database closes the connection
    conn.close.assert_called_once()

@patch("sqlite3.connect")
def test_query_db_mocked_connection(mock_connection):
    """Mock the database connection and cursor to ensure the correct methods
    are called within the query_database function
    """
    mock_cursor = mock_connection.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [("Jerry", "Mouse", 1)]
    # make our fake connection
    conn = mock_connection("my_non_existent_file")
    sql = "SELECT * FROM Animals"
    # test what query_database does with our fake connection
    result = query_database(sql, conn=conn)
    assert result[0] == ("Jerry", "Mouse", 1)
    # check that query_database passes our SQL string to cursor.execute()
    mock_cursor.execute.assert_called_once_with(sql)
    # check that fetchall() was called
    mock_cursor.fetchall.assert_called_once()
    # check that query_database closes the connection
    conn.close.assert_called_once()

@pytest.fixture(scope="session")
def setup_database(database_connection):
    """
    Populate data in database
    """
    conn = database_connection
    cur = conn.cursor()
    cur.execute("CREATE TABLE Animals(Name, Species, Age)")
    cur.execute("INSERT INTO Animals VALUES ('Bugs', 'Rabbit', 6)")
    conn.commit()
    yield conn
    cur.execute("DROP TABLE Animals")

def test_connect_to_db_type(database_fn_fixture):
    """
    Test that connect_to_db function returns sqlite3.Connection
    """
    conn = connect_to_database(database_fn_fixture)
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

def test_connect_to_db_name(database_fn_fixture):
    """
    Test that connect_to_db function connects to correct DB file
    """
    conn = connect_to_database(database_fn_fixture)
    cur = conn.cursor()
    # List current databases https://www.sqlite.org/pragma.html#pragma_database_list
    cur.execute("PRAGMA database_list;")
    # Unpack the three parameters returned
    db_index, db_type, db_filepath = cur.fetchone()
    # Test that the database filename is the same as the one from the fixture
    assert Path(db_filepath).name == Path(database_fn_fixture).name
    conn.close()

def test_query_database(setup_database):
    """
    Test that query_database retrieves the correct data
    """
    conn = setup_database
    sql = "SELECT * FROM Animals"
    result = query_database(sql, conn=conn)
    # Result returned is a list (cursor.fetchall)
    assert isinstance(result, list)
    # There should just be one record
    assert len(result) == 1
    # That record should be the data we added
    assert result[0] == ("Bugs", "Rabbit", 6)

def test_query_database_without_connection():
    """
    Test the `query_database` function without a provided connection
    """
    sql = 'SELECT * FROM Animals'
    # ensure that we get a TypeError
    with pytest.raises(TypeError):
        query_database(sql)