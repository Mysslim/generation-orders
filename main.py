import logging
import configparser

from settings.constants import FORMAT_FOR_LOGGER
from generators import *

def setup_logger(config):
    logging.basicConfig(
        filename = config["logging"]["PATH_TO_LOG_FILE"],
        filemode = config["logging"]["FILE_MODE_LOG"],
        level = config["logging"]["LEVEL_LOG"],
        format = FORMAT_FOR_LOGGER)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("settings/config.ini")
    setup_logger(config)

    al = GeneratorHistoryRecord(config)

    al.already_open_orders()
    # al.completed_orders()
    # al.unfinished_orders()
