
from datetime import datetime
from constants import *
from helper_method import *

def genering_id_orders(config):
    id_orders = []
    pseudo_gen_volume = pseudo_genering_volumes_int(config, COUNT_ORDERS, "id_order")
    
    for volume in pseudo_gen_volume :
        id_orders.append(hex(int(volume)))

    return id_orders

def genering_id_instruments(config):
    instruments = []
    pseudo_gen_volume = pseudo_genering_volumes_int(config, COUNT_ORDERS, "instrument")
    
    for order in range(0, COUNT_ORDERS):
        instruments.append(pseudo_gen_volume[order])

    return instruments

def genering_pxs_fill(config):
    pxs_fill = []
    id_instruments = genering_id_instruments(config)
    comma_wrap = float(config["comma_wrap"]["IN_DIFFERENCE_PX_FILL"])
    count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_PX_FILL"])
    pseudo_gen_volumes = pseudo_genering_volumes_float(config, COUNT_ORDERS, "px_fill")

    for order in range(0, COUNT_ORDERS):
        id_instrument = id_instruments[order]
        px_init = get_volume_via_id(INSTRUMENTS, id_instrument)[1]
        difference = pseudo_gen_volumes[order] * comma_wrap

        px_fill = 0.0

        if pseudo_gen_volumes[order] % 3 == 0:
            px_fill = px_init - difference
        else:
            px_fill = px_init + difference
        
        px_fill = round(px_fill, count_before_comma)
        pxs_fill.append(px_fill)
    
    return pxs_fill        
            
def genering_sides(config):
    sides = []
    pseudo_gen_volumes = pseudo_genering_volumes_int(config, COUNT_ORDERS, "side")
    
    for order in range(0, COUNT_ORDERS):
        side = "null"
        if pseudo_gen_volumes[order] % 3 == 0:
            side = SIDES[0]
        else:
            side = SIDES[1]

        sides.append(side)

    return sides

def genering_volumes_init(config):
    volumes_init = []
    comma_wrap = float(config["comma_wrap"]["IN_VOLUME_INIT"])
    count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_VOLUME_INIT"])
    pseudo_gen_volumes = pseudo_genering_volumes_float(config, COUNT_ORDERS, "volume_init")

    for order in range (0, COUNT_ORDERS):
        volume_init = pseudo_gen_volumes[order] * comma_wrap
        volume_init = round(volume_init, count_before_comma)
        volumes_init.append(volume_init)

    return volumes_init

def genering_volumes_fill(config):
    volumes_fill = []
    volumes_init = genering_volumes_init(config)
    comma_wrap = float(config["comma_wrap"]["IN_VOLUME_FILL"]) 
    pseudo_gen_volumes = pseudo_genering_volumes_float(config, COUNT_ORDERS, "volume_fill")

    for order in range(0, COUNT_ORDERS):
        difference = pseudo_gen_volumes[order] * comma_wrap
        volume_fill = abs(volumes_init[order] - difference)

        if volume_fill > volumes_init[order]:
            volume_fill = volumes_init[order]
        
        volume_fill = round(volume_fill, 7)
        volumes_fill.append(volume_fill)

    return volumes_fill

def genering_dates(config):
    dates = []
    pseudo_gen_volumes_for_date = pseudo_genering_volumes_float(config, COUNT_RECORDS, "date")

    for record in range(0, COUNT_RECORDS):
        date_record = datetime.fromtimestamp(pseudo_gen_volumes_for_date[record] + STARTING_POINT)
        microsecond = date_record.microsecond
        date = "{}.{}".format(date_record.strftime(FORMAT_DATA_WITHOUT_MICROSECOND), str(microsecond)[:3])
        dates.append(date)

    dates.sort()
    return dates

def genering_statuses(config):
    statuses = []
    volumes_init = genering_volumes_init(config)
    volumes_fill = genering_volumes_fill(config)
    pseudo_gen_volumes = pseudo_genering_volumes_int(config, COUNT_ORDERS, "status")
    status = "null"

    for order in range(0, COUNT_ORDERS):
        if volumes_fill[order] == volumes_init[order]:
            status = STATUSES[2]
        else:
            status = choice_of_status(pseudo_gen_volumes[order])
        
        statuses.append(status)

    return statuses

def genering_notes(config):
    notes = []
    pseudo_gen_volumes = pseudo_genering_volumes_int(config, COUNT_ORDERS, "note")

    for order in range(0, COUNT_ORDERS):
        notes.append(pseudo_gen_volumes[order])

    return notes

def genering_combinations_of_tags(config):
    combination_of_tags = []
    count_tags = TAGS.__len__()
    
    count_pseudo_gen_volumes = count_tags * COUNT_COMBINATION_OF_TAGS
    pseudo_gen_volumes = pseudo_genering_volumes_float(config, count_pseudo_gen_volumes, "array_tag")

    for combination in range(0, COUNT_COMBINATION_OF_TAGS):
        tags = ""
        for tag in range(0, count_tags):
            index_for_volume = combination + tag

            if pseudo_gen_volumes[index_for_volume] % 2 == 0:
                tags += TAGS[tag] + " "
        
        combination_of_tags.append(tags)
            
    return combination_of_tags

def genering_tags(config):
    tags = []
    combinations_of_tags = genering_combinations_of_tags(config)
    pseudo_gen_volumes = pseudo_genering_volumes_int(config, COUNT_ORDERS, "tag")

    for order in range(0, COUNT_ORDERS):
        id_combination_tags = pseudo_gen_volumes[order]
        combination_tags = combinations_of_tags[id_combination_tags]

        tags.append(combination_tags)  

    return tags