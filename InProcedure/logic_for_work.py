import csv
import logging

from datetime import datetime
from constants import *

def setup_logger(config):
    logging.basicConfig(
        filename = config["logging"]["PATH_TO_LOG_FILE"],
        filemode = config["logging"]["FILE_MODE_LOG"],
        level = config["logging"]["LEVEL_LOG"],
        format = FORMAT_FOR_LOGGER)

def check_config(config):
    try:
        config.read("setting/config.ini")
    
    except FileNotFoundError:

        logging.error("Config is not exists, used default config!!!")
        config.read("setting/default_config.ini")

def get_volume_by_id(list, id):
    return list[id]

def choice_of_status(volume):
    if volume % 2 == 0:
        status = STATUSES[3]
    else:
        status = STATUSES[4]

    return status

def congruent_method(x_previos, a, c, M):
    return (a * x_previos + c) % M

def get_volume_for_congruent_method_with_config(config, section, type_name):
    try:
        seed = type_name(config[section]["SEED"])
        a = type_name(config[section]["A"])
        c = type_name(config[section]["C"])
        m = type_name(config[section]["M"])

    except Exception:
        logging.error("\"type_name\" must be a numeric type: int, float")
        seed = 1
        a = 2
        c = 3
        m = 4

    return (seed, a, c, m)

def get_correct_volume_by_status(current_volume, correct_volume, status):
    if status == STATUSES[2] or status == STATUSES[3]:
        return current_volume
    return correct_volume

def write_orders_in_history(history_records, order_index, record_index, count_orders, genering_volume):
    # genering_volume[0] = id_orders
    # genering_volume[1] = id_instruments
    # genering_volume[2] = pxs_fill
    # genering_volume[3] = sides
    # genering_volume[4] = volumes_init
    # genering_volume[5] = volumes_fill
    # genering_volume[6] = dates
    # genering_volume[7] = statuses
    # genering_volume[8] = notes
    # genering_volume[9] = tags
    
    index_for_date = 0 # because dates is 7200, others genering volume = 2000
    for order_index in range(order_index, count_orders + order_index):
        array_of_statuses = TEMPLATE_FOR_STATUS[count_orders]
        
        logging.debug("Start adding new record, record: {}".format(record_index))
        for status in array_of_statuses:

            quotation = get_volume_by_id(INSTRUMENTS, genering_volume[1][order_index])[0]
            px_init = get_volume_by_id(INSTRUMENTS, genering_volume[1][order_index])[1]
            status = get_correct_volume_by_status(genering_volume[7][order_index], status, status)
            px_fill = get_correct_volume_by_status(genering_volume[2][order_index], 0, status)
            volume_fill = get_correct_volume_by_status(genering_volume[5][order_index], 0, status)
            
            volumes = [
                    record_index, 
                    genering_volume[0][order_index], 
                    quotation,
                    px_init,
                    px_fill,
                    genering_volume[3][order_index],
                    genering_volume[4][order_index],
                    volume_fill,
                    genering_volume[6][index_for_date],
                    status,
                    genering_volume[8][order_index],
                    genering_volume[9][order_index]]
            
            index_for_date += 1
            try:
                history_records.append(volumes)

                logging.debug("Add new record in history, record: {}".format(record_index))

            except:
                logging.error("Record not added in history, volumes: {0}".format(volumes))

            record_index += 1
    
    logging.debug("order_index = {}, record_index = {}".format(order_index, record_index))
    return order_index, record_index

def get_all_genering_volumes(config):
    return (genering_id_orders(config),
            genering_id_instruments(config),
            genering_pxs_fill(config),
            genering_sides(config),
            genering_volumes_init(config),
            genering_volumes_fill(config),
            genering_dates(config),
            genering_statuses(config),
            genering_notes(config),
            genering_tags(config))

def pseudo_genering_volumes(config, count_orders, section, type_name):
    volumes = []

    x_previos, a, c, M = get_volume_for_congruent_method_with_config(config, section, type_name)
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

    logging.info("Pseudo genereting volumes is end")
    return volumes

def genering_id_orders(config):
    id_orders = []
    pseudo_gen_volume = pseudo_genering_volumes(config, COUNT_ORDERS, "id_order", int)
    
    for volume in pseudo_gen_volume :
        id_orders.append(hex(volume))

    logging.info("Id_orders is generated")
    return id_orders

def genering_id_instruments(config):
    instruments = []
    pseudo_gen_volume = pseudo_genering_volumes(config, COUNT_ORDERS, "instrument", int)
    
    for order in range(0, COUNT_ORDERS):
        instruments.append(pseudo_gen_volume[order])

    logging.info("Id_instruments is generated")
    return instruments

def genering_pxs_fill(config):
    pxs_fill = []
    id_instruments = genering_id_instruments(config)
    comma_wrap = float(config["comma_wrap"]["IN_DIFFERENCE_PX_FILL"])
    count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_PX_FILL"])
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "px_fill", int)

    for order in range(0, COUNT_ORDERS):
        id_instrument = id_instruments[order]
        px_init = get_volume_by_id(INSTRUMENTS, id_instrument)[1]
        difference = pseudo_gen_volumes[order] * comma_wrap

        px_fill = 0.0

        if pseudo_gen_volumes[order] % 3 == 0:
            px_fill = px_init - difference
        else:
            px_fill = px_init + difference
        
        px_fill = round(px_fill, count_before_comma)
        pxs_fill.append(px_fill)
    
    logging.info("Pxs fill is generated")
    return pxs_fill        
            
def genering_sides(config):
    sides = []
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "side", int)
    
    for order in range(0, COUNT_ORDERS):
        side = "null"
        if pseudo_gen_volumes[order] % 3 == 0:
            side = SIDES[0]
        else:
            side = SIDES[1]

        sides.append(side)

    logging.info("Sides is generated")
    return sides

def genering_volumes_init(config):
    volumes_init = []
    comma_wrap = float(config["comma_wrap"]["IN_VOLUME_INIT"])
    count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_VOLUME_INIT"])
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "volume_init", float)

    for order in range (0, COUNT_ORDERS):
        volume_init = pseudo_gen_volumes[order] * comma_wrap
        volume_init = round(volume_init, count_before_comma)
        volumes_init.append(volume_init)

    logging.info("Volumes init is generated")
    return volumes_init

def genering_volumes_fill(config):
    volumes_fill = []
    volumes_init = genering_volumes_init(config)
    comma_wrap = float(config["comma_wrap"]["IN_VOLUME_FILL"]) 
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "volume_fill", float)

    for order in range(0, COUNT_ORDERS):
        difference = pseudo_gen_volumes[order] * comma_wrap
        volume_fill = abs(volumes_init[order] - difference)

        if volume_fill > volumes_init[order]:
            volume_fill = volumes_init[order]
        
        volume_fill = round(volume_fill, 7)
        volumes_fill.append(volume_fill)

    logging.info("Volumes fill is generated")
    return volumes_fill

def genering_dates(config):
    dates = []
    pseudo_gen_volumes_for_date = pseudo_genering_volumes(config, COUNT_RECORDS, "date", float)

    for record in range(0, COUNT_RECORDS):
        date_record = datetime.fromtimestamp(pseudo_gen_volumes_for_date[record] + STARTING_POINT)
        microsecond = date_record.microsecond
        date = "{}.{}".format(date_record.strftime(FORMAT_DATA_WITHOUT_MICROSECOND), str(microsecond)[:3])
        dates.append(date)

    dates.sort()
    logging.info("Dates is generated")
    return dates

def genering_statuses(config):
    statuses = []
    volumes_init = genering_volumes_init(config)
    volumes_fill = genering_volumes_fill(config)
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "status", float)
    status = "null"

    for order in range(0, COUNT_ORDERS):
        if volumes_fill[order] == volumes_init[order]:
            status = STATUSES[2]
        else:
            status = choice_of_status(pseudo_gen_volumes[order])
        
        statuses.append(status)

    logging.info("Statuses is generated")
    return statuses

def genering_notes(config):
    notes = []
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "note", int)

    for order in range(0, COUNT_ORDERS):
        note = get_volume_by_id(NOTES, pseudo_gen_volumes[order])
        notes.append(note)

    logging.info("Notes is generated")
    return notes

def genering_combinations_of_tags(config):
    combination_of_tags = []
    count_tags = TAGS.__len__()
    
    count_pseudo_gen_volumes = count_tags * COUNT_COMBINATION_OF_TAGS
    pseudo_gen_volumes = pseudo_genering_volumes(config, count_pseudo_gen_volumes, "array_tag", float)

    for combination in range(0, COUNT_COMBINATION_OF_TAGS):
        tags = ""
        for tag in range(0, count_tags):
            index_for_volume = combination + tag

            if pseudo_gen_volumes[index_for_volume] % 2 == 0:
                tags += TAGS[tag] + " "
        
        combination_of_tags.append(tags)

    logging.info("Combination of tags is generated")    
    return combination_of_tags

def genering_tags(config):
    tags = []
    combinations_of_tags = genering_combinations_of_tags(config)
    pseudo_gen_volumes = pseudo_genering_volumes(config, COUNT_ORDERS, "tag", int)

    for order in range(0, COUNT_ORDERS):
        id_combination_tags = pseudo_gen_volumes[order]
        combination_tags = combinations_of_tags[id_combination_tags]

        tags.append(combination_tags)  

    logging.info("Tags is generated")
    return tags

def get_history_records(config):
    history_records = []
    genering_volume = get_all_genering_volumes(config)
    
    order = 0
    record = 0

    order, record = write_orders_in_history(history_records, order, record, COUNT_STARTED_ORDERS, genering_volume)
    order, record = write_orders_in_history(history_records, order, record, COUNT_FULL_ORDERS, genering_volume)
    order, record = write_orders_in_history(history_records, order, record, COUNT_UNFINISH_ORDERS, genering_volume)

    logging.info("History record is get")
    return history_records

def get_attribute_of_tables(config):
    id = config["volume_for_dump"]["ID_RESULT"]
    id_order = config["volume_for_dump"]["ID_ORDER"]
    instrument = config["volume_for_dump"]["INSTRUMENT"]    
    px_init = config["volume_for_dump"]["PX_INIT"]
    px_fill = config["volume_for_dump"]["PX_FILL"]
    side = config["volume_for_dump"]["SIDE"]
    volume_init = config["volume_for_dump"]["VOLUME_INIT"]
    volume_fill = config["volume_for_dump"]["VOLUME_FILL"]
    date = config["volume_for_dump"]["DATE"]
    status = config["volume_for_dump"]["STATUS"]
    note = config["volume_for_dump"]["NOTE"]
    tag = config["volume_for_dump"]["TAG"]

    return id, id_order, instrument, px_init, px_fill, side, volume_init, volume_fill, date, status, note, tag

def write_to_csv(history_records, config):
    name_of_columns = get_attribute_of_tables(config)

    with open(config["csv"]["PATH_TO_CSV"], mode= "w", encoding="utf-8") as csv_file:
        file_writer = csv.writer(csv_file, delimiter = '\t', lineterminator = "\r")
        file_writer.writerow(name_of_columns)

        for record in history_records:
            row = []
            for element_of_record in record:
                row.append(element_of_record)
            file_writer.writerow(row)

    