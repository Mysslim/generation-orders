import logging
from abc import abstractmethod

class Repository:
    @abstractmethod
    def insert(self, generate_record):
        pass

    @abstractmethod
    def delete(self, generate_record):
        pass

    @abstractmethod
    def update(self, generate_record):
        pass

class MySqlRepository(Repository):
    pass

class CSVRepository(Repository):
    pass