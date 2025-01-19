import sqlite3

from src.data.idatabase import IDatabase


class SQLiteDatabase(IDatabase):
    __connection: sqlite3.Connection = None

    @classmethod
    def connect(cls, name: str):
        cls.database_name = name
        cls.connection = sqlite3.connect(cls.database_name)

    @classmethod
    def get_cursor(cls):
        yield cls.connection.cursor()
