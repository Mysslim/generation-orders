import logging
import configparser
from storages import MySqlRepository

from settings.constants import FORMAT_FOR_LOGGER
from builder import BuilderGeneratorAsset

def setup_logger(config):
    logging.basicConfig(
        filename = config["logging"]["PATH_TO_LOG_FILE"],
        filemode = config["logging"]["FILE_MODE_LOG"],
        level = config["logging"]["LEVEL_LOG"],
        format = FORMAT_FOR_LOGGER)

def setup_config():
    config = configparser.ConfigParser()

    try:
        config.read("settings/config.ini")
    except FileNotFoundError:
        logging.error("config not found, stop working")
    
    return config

def setup():
    
    config = setup_config()
    setup_logger(config)

    return config

def workflow(config):

    build = BuilderGeneratorAsset(config)
    repository = MySqlRepository(config)
    repository.setup()

    for strategy in range(build.get_count_strategies()):
        for asset in range(build.get_count_assets(strategy)):
            records = MappingAssetInRecord.get_records_from_asset(build.get_asset(strategy))

            repository.insert(records)

    repository.close

if __name__ == "__main__":
    config = setup()
    workflow(config)

    

