import configparser
import logging

from genering import *

def setup():
    global config, comma_wrap_for_px_fill, count_before_comma_for_px_fill
    global comma_wrap_for_volume_init, count_before_comma_volume_init, comma_wrap_for_volume_fill
    
    config = configparser.ConfigParser()
    config.read("config.ini")

    comma_wrap_for_px_fill = float(config["comma_wrap"]["IN_DIFFERENCE_PX_FILL"])
    count_before_comma_for_px_fill = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_PX_FILL"])
    comma_wrap_for_volume_init = float(config["comma_wrap"]["IN_VOLUME_INIT"])
    count_before_comma_volume_init = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_VOLUME_INIT"])
    comma_wrap_for_volume_fill = float(config["comma_wrap"]["IN_VOLUME_FILL"])

def start():
    genering_id_orders(config)
    genering_id_instruments(config)
    genering_combinations_of_tags(config)
    genering_dates(config)
    genering_notes(config)
    genering_pxs_fill(config)
    genering_sides(config)
    genering_statuses(config)
    genering_tags(config)
    genering_volumes_fill(config)
    genering_volumes_init(config)

if __name__ == "__main__":
    setup()
    start()
    