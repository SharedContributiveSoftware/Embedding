import sqlite3

import conftest
import pytest

from src.data.sqlitedatabase import SQLiteDatabase


def test_connect():
    SQLiteDatabase.connect(conftest.TEST_DB_PATH)

def test_get_cursor_without_connection():
    SQLiteDatabase.disconnect()

    with pytest.raises(ValueError):
        with SQLiteDatabase.get_cursor() as cursor:
            pass

def test_get_cursor():
    SQLiteDatabase.connect(conftest.TEST_DB_PATH)

    with SQLiteDatabase.get_cursor() as cursor:
        assert isinstance(cursor, sqlite3.Cursor)