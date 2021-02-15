import configparser
import json
from os import stat

def init():
    global config

    config = None

def setup():
    global config

    config = configparser.ConfigParser()
    config.read("config.ini")

# def get_all_count_records():
#     persent_started = int(config["some_setting"]["PERSENT_STARTED_ORDERS"])
#     persent_unfinish = int(config["some_setting"]["PERSENT_UNFINISH_ORDERS"])

#     if persent_started + persent_unfinish >= 100:

def congruent_method(x_previos, a, c, M):
    return (int(a) * int(x_previos) + int(c)) % int(M)

def get_volume_for_congruent_method_with_config(partition):
    return (float(config[partition]["SEED"]), 
           float(config[partition]["A"]),
           float(config[partition]["C"]),
           float(config[partition]["M"]))

def get_volume_via_id_and_key(id, key, path_to):
    volumes = get_volume_with_JSON(path_to)
    return volumes[id][key]

def get_volume_with_JSON(path_to):
    path_to_json = config["path_to"][path_to]
    with open(path_to_json, "r") as JSON_file:
        volumes = json.load(JSON_file)
        for volume in volumes:
            return volumes[volume]
        
def pseudo_genering_volumes(count_orders, partition):
    volumes = []

    x_previos, a, c, M = get_volume_for_congruent_method_with_config(partition)
    x_current = congruent_method(
        x_previos = x_previos,
        a = a,
        c = c,
        M = M)

    for order in range(0, count_orders):
        volumes.append(x_current)

        x_previos = x_current
        x_current = congruent_method(
            x_previos = x_previos,
            a = a,
            c = c,
            M = M)

    return volumes

def genering_id_orders():
    id_orders = []
    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    pseudo_gen_volume = pseudo_genering_volumes(count_orders, "id_order")
    
    for volume in pseudo_gen_volume :
        id_orders.append(hex(volume))

    return id_orders

def genering_instruments():
    instruments = {}
    id_orders = genering_id_orders()

    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    pseudo_gen_volume = pseudo_genering_volumes(count_orders, "instrument")
    
    for order in range(0, count_orders):
        instruments.update({id_orders[order]: pseudo_gen_volume[order]})

    return instruments
    
def genering_pxs_fill():
    pxs_fill = {}
    id_orders = genering_id_orders()
    instruments = genering_instruments()
    comma_wrap = float(config["comma_wrap"]["IN_DIFFERENCE_PX_FILL"])
    count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_PX_FILL"])
    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    pseudo_gen_volumes = pseudo_genering_volumes(count_orders, "px_fill")

    for order in range(0, count_orders):
        difference = pseudo_gen_volumes[order] * comma_wrap
        px_init = get_volume_via_id_and_key(instruments[id_orders[order]], "course", "JSON_FILE_INSTRUMENT")
        px_fill = 0.0

        if pseudo_gen_volumes[order] % 3 == 0:
            px_fill = px_init - difference
        else:
            px_fill = px_init + difference
        
        px_fill = round(px_fill, count_before_comma)
        pxs_fill.update({id_orders[order] : px_fill})
    
    return pxs_fill        
            
def genering_sides():
    sides = {}
    id_orders = genering_id_orders()
    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    pseudo_gen_volumes = pseudo_genering_volumes(count_orders, "side")
    
    for order in range(0, count_orders):
        side = "null"
        if pseudo_gen_volumes[order] % 3 == 0:
            side = "Buy"
        else:
            side = "Sell"

        sides.update({id_orders[order]: side})

    return sides

def genering_volumes_init():
    volumes_init = {}
    comma_wrap = float(config["comma_wrap"]["IN_VOLUME_INIT"])
    count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_VOLUME_INIT"])
    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    id_orders = genering_id_orders()
    pseudo_gen_volumes = pseudo_genering_volumes(count_orders, "volume_init")

    for order in range (0, count_orders):
        volume_init = pseudo_gen_volumes[order] * comma_wrap
        volume_init = round(volume_init, count_before_comma)
        volumes_init.update({id_orders[order]: volume_init})

    return volumes_init

def genering_volumes_fill():
    volumes_fill = {}
    id_orders = genering_id_orders()
    volumes_init = genering_volumes_init()
    comma_wrap = float(config["comma_wrap"]["IN_VOLUME_FILL"])
    count_orders = int(config["some_setting"]["COUNT_ORDERS"]) 
    pseudo_gen_volumes = pseudo_genering_volumes(count_orders, "volume_fill")

    for order in range(0, count_orders):
        difference = pseudo_gen_volumes[order] * comma_wrap
        id_order = id_orders[order]
        volume_fill = abs(volumes_init[id_order] - difference)

        if volume_fill > volumes_init[id_order]:
            volume_fill = volumes_init[id_order]
        
        volume_fill = round(volume_fill, 7)
        volumes_fill.update({id_orders[order] : volume_fill})

    return volumes_fill

def genering_dates():
    dates = {}

    return dates

def genering_statuses():
    statuses = {}
    id_orders = genering_id_orders()
    volumes_init = genering_volumes_init()
    volumes_fill = genering_volumes_fill()
    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    pseudo_gen_volumes = pseudo_genering_volumes(count_orders, "status")
    status = "null"

    for order in range(0, count_orders):
        id_order = id_orders[order]
        if volumes_fill[id_order] == volumes_init[id_order]:
            status = "Fill"
        else:
            if pseudo_gen_volumes[order] % 2 == 0:
                status = "ParticalFill"
            else: 
                status = "Cancel"
        
        statuses.update({id_order : status})

    return statuses

def genering_notes():
    notes = {}
    id_orders = genering_id_orders()
    count_orders = int(config["some_setting"]["COUNT_ORDERS"])
    pseudo_gen_volumes = pseudo_genering_volumes(count_orders, "note")

    for order in range(0, count_orders):
        id_order = id_orders[order]
        notes.update({id_order: pseudo_gen_volumes[order]})

    return notes

if __name__ == "__main__":
    init()
    setup()
    print(genering_notes())