import json
import logging
from settings.constants import PATH_TO_JSON


class JsonGetter:
    default_path = PATH_TO_JSON

    def get_volume(name_array, num_element, element):
        with open(PATH_TO_JSON, 'r') as json_file:
            dict = json.loads(json_file.read())
            
            if num_element >= len(dict[name_array]):
                num_element = len(dict[name_array]) - 1

            volume = dict[name_array][int(num_element) - 1][element]
            logging.debug("get volume in json num_element: {0}, volume: {1}".format(num_element, volume))
            return volume

    def get_count_of_name_array(name_array):
        with open(PATH_TO_JSON, 'r') as json_file:
            dict = json.loads(json_file.read())
            return len(dict[name_array])
