import sqlite3
from contextlib import contextmanager
from typing import Optional

from src.data.idatabase import IDatabase


class SQLiteDatabase(IDatabase):
    _connection: sqlite3.Connection = None

    @classmethod
    def connect(cls, name: str):
        cls.database_name = name
        cls._connection = sqlite3.connect(cls.database_name)

    @classmethod
    def disconnect(cls):
        if cls._connection is None:
            return

        cls._connection.close()
        cls._connection = None

    @classmethod
    @contextmanager
    def get_cursor(cls) -> Optional[sqlite3.Cursor]:
        if cls._connection is None:
            raise ValueError("Database connection is not setted")

        yield cls._connection.cursor()
