from abc import ABC, abstractmethod


class IDatabase(ABC):
    database_name: str = None
    connection_name: str = None

    @classmethod
    @abstractmethod
    def connect(cls, name: str):
        raise NotImplementedError("Not implemented yet")

    @classmethod
    @abstractmethod
    def disconnect(cls):
        raise NotImplementedError("Not implemented yet")

    @classmethod
    @abstractmethod
    def get_connection_name(cls):
        return cls.connection_name

    @classmethod
    @abstractmethod
    def get_database_name(cls):
        return cls.database_name

    @classmethod
    @abstractmethod
    def get_cursor(cls):
        raise NotImplementedError("Not implemented yet")