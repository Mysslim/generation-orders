import logging

from abc import abstractmethod

from pymysql import connect
import pymysql
from mysql_connector import MySQLConnector


class Repository:
    @abstractmethod
    def insert(self, records):
        pass

    @abstractmethod
    def delete(self, records):
        pass

    @abstractmethod
    def update(self, records):
        pass

class MySqlRepository(Repository):
    def __init__(self, config) -> None:
        self.__connector = MySQLConnector(config)
        self.__config = config

    def setup(self):
        self.__connector.create_database()
        self.__connector.use_database()
        self.__connector.create_table()
        
    def close(self):
        self.__connector.close_connection()

    def insert(self, records):
        for record in records:
            insert = """INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11})""".format(
                self.__config["volume_for_dump"]["TABLE"], 
                self.__config["volume_for_dump"]["ID_ORDER"],
                self.__config["volume_for_dump"]["INSTRUMENT"],
                self.__config["volume_for_dump"]["PX_INIT"],
                self.__config["volume_for_dump"]["PX_FILL"],
                self.__config["volume_for_dump"]["VOLUME_INIT"],
                self.__config["volume_for_dump"]["VOLUME_FILL"],
                self.__config["volume_for_dump"]["SIDE"],
                self.__config["volume_for_dump"]["STATUS"],
                self.__config["volume_for_dump"]["DATE"],
                self.__config["volume_for_dump"]["NOTE"],
                self.__config["volume_for_dump"]["TAG"])
            
            values = """
                 VALUES('{0}', '{1}', {2}, {3}, {4}, {5}, '{6}', '{7}', '{8}', '{9}', '{10}');
                """.format(
                record.id_order,
                record.quotation,
                record.px_init,
                record.px_fill,
                record.volume_init,
                record.volume_fill,
                record.side,
                record.status,
                record.date,
                record.note,
                record.tags)

            query = insert + values
            logging.info("make query for insert data, id {0}".format(record.id_order))

            try:
                self.__connector.execute_query(query)
                logging.info("execute query id: {0}".format(record.id_order))

            except pymysql.err.ProgrammingError as ex:
                logging.error(ex, "an internal error has occurred, stoped insering")
                return
            
            except Exception as ex:
                logging.error(ex, "skip insert, id: {0}".format(record.id_order))
                continue

class CSVRepository(Repository):
    pass