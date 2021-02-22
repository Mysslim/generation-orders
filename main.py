import configparser
from method_for_work import *

def setup():

    config = configparser.ConfigParser()
    check_config(config)
    setup_logger(config)

    return config

def start(config):
    history_records = get_history_records(config)
    write_to_csv(history_records, config)

if __name__ == "__main__":
    config = setup()
    start(config)