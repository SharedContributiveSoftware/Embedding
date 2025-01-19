import sqlite3

from src.data.idatabase import IDatabase


class SQLiteDatabase(IDatabase):
    __connection: sqlite3.Connection = None

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
    def get_cursor(cls):
        yield cls.connection.cursor()
