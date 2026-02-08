# coding=utf-8
import pytest
import sqlite3
from bcminer.db_manager import DatabaseManager
from bcminer.db_manager import TokenExistsException


@pytest.fixture
def db_manager() -> DatabaseManager:
    db_path = "test.db"
    return DatabaseManager(db_path)

@pytest.fixture(autouse=True)
def cleanup_db(db_manager: DatabaseManager) -> None:
    with sqlite3.connect(db_manager.db_name) as connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS tokens")
        connection.commit()

@pytest.fixture
def connection() -> sqlite3.Connection:
    return sqlite3.connect("test.db")

@pytest.fixture
def cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    return connection.cursor()

@pytest.fixture
def prepared_db(db_manager: DatabaseManager, cursor: sqlite3.Cursor) -> None:
    db_manager.create_tables()
    cursor.execute("INSERT INTO tokens (version, owner, randdata, hash) VALUES ('testversion', 'Alice', 1, 'hash1')")
    cursor.execute("INSERT INTO tokens (version, owner, randdata, hash) VALUES ('testversion', 'Bob', 2, 'hash2')")
    connection = cursor.connection
    connection.commit()

def test_create_tables(db_manager: DatabaseManager, cursor: sqlite3.Cursor) -> None:
    db_manager.create_tables()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tokens'")
    assert cursor.fetchone() is not None

def test_get_tokens(prepared_db: None, db_manager: DatabaseManager) -> None:
    tokens = db_manager.get_tokens()
    assert tokens == [(1, 'testversion', 'Alice', "1", 'hash1'), (2, 'testversion', 'Bob', "2", 'hash2')]

def test_get_user_tokens(prepared_db: None, db_manager: DatabaseManager) -> None:
    alice_tokens = db_manager.get_user_tokens("Alice")
    bob_tokens = db_manager.get_user_tokens("Bob")
    assert alice_tokens == [(1, 'testversion', 'Alice', "1", 'hash1')]
    assert bob_tokens == [(2, 'testversion', 'Bob', "2", 'hash2')]

def test_get_user_tokens_no_tokens(prepared_db: None, db_manager: DatabaseManager) -> None:
    charlie_tokens = db_manager.get_user_tokens("Charlie")
    assert charlie_tokens == []

def test_insert_token(prepared_db: None, db_manager: DatabaseManager, cursor: sqlite3.Cursor) -> None:
    db_manager.insert_token('testversion', "Charlie", "3", "hash3")
    cursor.execute("SELECT * FROM tokens")
    tokens = cursor.fetchall()
    assert tokens == [(1, 'testversion', 'Alice', "1", 'hash1'), (2, 'testversion', 'Bob', "2", 'hash2'),
                      (3, 'testversion', 'Charlie', "3", 'hash3')]

def test_insert_existing_token(prepared_db: None, db_manager: DatabaseManager) -> None:
    with pytest.raises(TokenExistsException):
        db_manager.insert_token('testversion', "Alice", "1", "hash1")
    with pytest.raises(TokenExistsException):
        db_manager.insert_token('testversion', "Alice", "1", "hash88")
