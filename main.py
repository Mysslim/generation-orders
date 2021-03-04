import configparser

from logic_for_work import *
from logic_for_SQL import *

def setup():

    config = configparser.ConfigParser()
    check_config(config)
    setup_logger(config)

    return config

def mysql_work(config):
    connection = get_connection(config)
    create_database(connection, config)
    use_database(connection, config)
    create_table(connection, config)
    write_to_mysql(connection, config)
    close_connection(connection)

def workflow(config):
    history_records = get_history_records(config)
    write_to_csv(history_records, config)
    mysql_work(config)

if __name__ == "__main__":
    config = setup()
    workflow(config)