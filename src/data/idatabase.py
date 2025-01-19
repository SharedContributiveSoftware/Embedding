from abc import ABC, abstractmethod

class IDatabase(ABC):
    database_name: str = None
    connection_name: str = None

    @classmethod
    @abstractmethod
    def connect(cls, name: str):
        raise NotImplementedError("Not implemented yet")

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError("Not implemented yet")

    def get_connection_name(self):
        return self.connection_name

    def get_database_name(self):
        return self.database_name

    @abstractmethod
    def get_cursor(self):
        raise NotImplementedError("Not implemented yet")