import pymysql
import csv
import logging

def get_connection(config):
    connection = pymysql.connect(
        host = config["volume_for_dump"]["HOST"],
        user = config["volume_for_dump"]["USER"],
        password = config["volume_for_dump"]["PASSWORD"],
        charset = config["volume_for_dump"]["CHARSET"]
    )

    return connection

def close_connection(connection):
    connection.close()

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)

    return cursor.description

def create_database(connection, config):
    query = """ 
    CREATE DATABASE IF NOT EXISTS {0};
    """.format(config["volume_for_dump"]["DATABASE"])
    
    execute_query(connection, query)

def use_database(connection, config):
    query = "use {0}".format(config["volume_for_dump"]["DATABASE"])

    execute_query(connection, query)

def create_table(connection, config):
    table = config["volume_for_dump"]["TABLE"]
    id = config["volume_for_dump"]["ID_RESULT"]
    id_order = config["volume_for_dump"]["ID_ORDER"]
    quotation  = config["volume_for_dump"]["INSTRUMENT"]
    px_init = config["volume_for_dump"]["PX_INIT"]
    px_fill = config["volume_for_dump"]["PX_FILL"]
    volume_init = config["volume_for_dump"]["VOLUME_INIT"]
    volume_fill = config["volume_for_dump"]["VOLUME_FILL"]
    side = config["volume_for_dump"]["SIDE"]
    status = config["volume_for_dump"]["STATUS"]
    date = config["volume_for_dump"]["DATE"]
    note = config["volume_for_dump"]["NOTE"]
    tag = config["volume_for_dump"]["TAG"]
    
    query = """
    CREATE TABLE IF NOT EXISTS {0} (
        {1} INT(5) PRIMARY KEY NOT NULL,
        {2} VARCHAR(10) NOT NULL,
        {3} ENUM('EUR/RUB', 'EUR/USD', 'EUR/JPY', 'USD/RUB', 'USD/UAH', 'GBP/UAH', 'USD/CHF', 'JPY/USD', 'GBP/USD', 'NZD/USD', 'USD/JPY') NOT NULL,
        {4} FLOAT(4) NOT NULL,
        {5} FLOAT(4),
        {8} ENUM('Sell', 'Buy') NOT NULL,
        {6} FLOAT(4),
        {7} FLOAT(4),
        {9} DATETIME(3) NOT NULL,
        {10} ENUM('New', 'InProcess', 'Fill', 'ParticalFill', 'Cancel', 'Done') NOT NULL,
        {11} VARCHAR(500),
        {12} VARCHAR(50))
    """.format(
        table, id, id_order, 
        quotation, px_init, 
        px_fill, volume_init, 
        volume_fill, side, 
        date, status,
        note, tag)

    execute_query(connection, query)

def write_to_mysql(connection, config):
    with open(config["csv"]["PATH_TO_CSV"], mode = 'r', encoding="utf-8") as csv_file:
        file_reader = csv.reader(csv_file, delimiter = '\t')
        for row in file_reader:
            
            # to skip the header line
            if row[0] == config["volume_for_dump"]["ID_RESULT"]:
                logging.info("skip header line in csv")
                continue

            query = """
            INSERT INTO 
            {0} VALUES({1}, '{2}', '{3}', {4}, {5}, '{6}', {7}, {8}, '{9}', '{10}', '{11}', '{12}');
            """.format(config["volume_for_dump"]["TABLE"], row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            logging.info("make query for insert data, record: {0}".format(row[0]))

            try:
                execute_query(connection, query)
                connection.commit()
            except Exception as ex:
                logging.error(ex, "skip this insert")
                continue


            

