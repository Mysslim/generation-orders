import configparser
import json

def init():
    global seed_for_id_order, a_for_id_order, c_for_id_order, M_for_id_order,
        seed_for_instrument, a_for_instrument, c_for_instrument, M_for_instrument,
        config

    config = None

    seed_for_id_order = None
    a_for_id_order = None
    c_for_id_order = None
    M_for_id_order = None

    seed_for_instrument = None
    a_for_instrument = None
    c_for_instrument = None
    M_for_instrument = None

def setup():
    global seed_for_id_order, a_for_id_order, c_for_id_order, M_for_id_order,
        seed_for_instrument, a_for_instrument, c_for_instrument, M_for_instrument,
        config

    config = configparser.ConfigParser()
    config.read("config.ini")

    seed_for_id_order = config["id_order"]["SEED"]
    a_for_id_order = config["id_order"]["A"]
    c_for_id_order = config["id_order"]["C"]
    M_for_id_order = config["id_order"]["M"]

    seed_for_instrument = config["instument"]["SEED"]
    a_for_instrument = config["instument"]["A"]
    c_for_instrument = config["instument"]["C"]
    M_for_instrument = config["instument"]["M"]


def congruent_method(x_previos, a, c, M):
    return (int(a) * int(x_previos) + int(c)) % int(M)

def genering_id_order():
    id_orders = []
    x_current = congruent_method(
        x_previos = seed_for_id_order,
        a = a_for_id_order,
        c = c_for_id_order,
        M = M_for_id_order)

    id_orders.append(hex(x_current))

    for order in range(1, 2000) :
        x_previos = x_current
        x_current = congruent_method(
            x_previos = x_previos,
            a = a_for_id_order,
            c = c_for_id_order,
            M = M_for_id_order)
        id_orders.append(hex(x_current))

    return id_orders

def genering_instrument():


if __name__ == "__main__":
    init()
    setup()
    genering_id_order()