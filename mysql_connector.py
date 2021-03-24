import pymysql
import logging

class MySQLConnector:
    def __init__(self, config) -> None:
        self.__config = config
        self.__connection = self.get_connection()

    def get_connection(self):
        try:
            connection = pymysql.connect(
                host = self.__config["volume_for_dump"]["HOST"],
                user = self.__config["volume_for_dump"]["USER"],
                password = self.__config["volume_for_dump"]["PASSWORD"],
                charset = self.__config["volume_for_dump"]["CHARSET"])
        except:
            logging.error("can`t connection on MySQL")

        return connection

    def close_connection(self):
        self.__connection.close()
        logging.info("connection of MySQL closed")

    def execute_query(self, query):
        cursor = self.__connection.cursor()
        cursor.execute(query)

        self.__connection.commit()
        return cursor.description

    def create_database(self):
        query = """ 
        CREATE DATABASE IF NOT EXISTS {0};
        """.format(self.__config["volume_for_dump"]["DATABASE"])
        
        self.execute_query(query)
        logging.debug("database created")

    def use_database(self):
        query = "use {0}".format(self.__config["volume_for_dump"]["DATABASE"])

        self.execute_query(query)
        logging.debug("database selected")

    def create_table(self):
        table = self.__config["volume_for_dump"]["TABLE"]
        id = self.__config["volume_for_dump"]["ID_RESULT"]
        id_order = self.__config["volume_for_dump"]["ID_ORDER"]
        quotation  = self.__config["volume_for_dump"]["INSTRUMENT"]
        px_init = self.__config["volume_for_dump"]["PX_INIT"]
        px_fill = self.__config["volume_for_dump"]["PX_FILL"]
        volume_init = self.__config["volume_for_dump"]["VOLUME_INIT"]
        volume_fill = self.__config["volume_for_dump"]["VOLUME_FILL"]
        side = self.__config["volume_for_dump"]["SIDE"]
        status = self.__config["volume_for_dump"]["STATUS"]
        date = self.__config["volume_for_dump"]["DATE"]
        note = self.__config["volume_for_dump"]["NOTE"]
        tag = self.__config["volume_for_dump"]["TAG"]
        
        query = """
        CREATE TABLE IF NOT EXISTS {0} (
            {1} INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT, 
            {2} VARCHAR(10) NOT NULL,
            {3} ENUM('EUR/RUB', 'EUR/USD', 'EUR/JPY', 'USD/RUB', 'USD/UAH', 'GBP/UAH', 'USD/CHF', 'JPY/USD', 'GBP/USD', 'NZD/USD', 'USD/JPY') NOT NULL,
            {4} FLOAT(4) NOT NULL,
            {5} FLOAT(4),
            {8} ENUM('Sell', 'Buy') NOT NULL,
            {6} FLOAT(4),
            {7} FLOAT(4),
            {9} DATETIME(3) NOT NULL,
            {10} ENUM('New', 'InProcess', 'Fill', 'ParticalFill', 'Cancel', 'Done') NOT NULL,
            {11} VARCHAR(255),
            {12} VARCHAR(100))
        """.format(
            table, id, id_order, 
            quotation, px_init, 
            px_fill, volume_init, 
            volume_fill, side, 
            date, status,
            note, tag)

        self.execute_query(query)
        logging.debug("table created")