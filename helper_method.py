from constants import *

def get_volume_via_id(list, id):
    return list[id]

def choice_of_status(volume):
    if volume % 2 == 0:
        status = STATUSES[3]
    else:
        status = STATUSES[4]

    return status

def congruent_method(x_previos, a, c, M):
    return (a * x_previos + c) % M

def get_volume_for_congruent_method_with_config_float(config, partition):
    return (float(config[partition]["SEED"]), 
           float(config[partition]["A"]),
           float(config[partition]["C"]),
           float(config[partition]["M"]))

def get_volume_for_congruent_method_with_config_int(config, partition):
    return (int(config[partition]["SEED"]), 
           int(config[partition]["A"]),
           int(config[partition]["C"]),
           int(config[partition]["M"]))

def pseudo_genering_volumes_float(config, count_orders, partition):
    volumes = []

    x_previos, a, c, M = get_volume_for_congruent_method_with_config_float(config, partition)
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

def pseudo_genering_volumes_int(config, count_orders, partition):

    volumes = []

    x_previos, a, c, M = get_volume_for_congruent_method_with_config_int(config, partition)
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

def get_quotation_by_id(id):
    return get_volume_via_id(INSTRUMENTS, id)[0]