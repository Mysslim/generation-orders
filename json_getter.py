import json
from os import name
from settings.constants import PATH_TO_JSON


class JsonGetter:
    default_path = PATH_TO_JSON

    def get_volume(name_array, num_element, element):
        with open(PATH_TO_JSON, 'r') as json_file:
            dict = json.loads(json_file.read())
            
            if num_element >= len(dict[name_array]):
                num_element = len(dict[name_array]) - 1

            return dict[name_array][int(num_element)][element]

    def get_count_of_name_array(name_array):
        with open(PATH_TO_JSON, 'r') as json_file:
            dict = json.loads(json_file.read())
            return len(dict[name_array])
