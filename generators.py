import logging

from DTO import DTOAsset
from abc import abstractmethod
from datetime import datetime
from json_getter import JsonGetter
from pseudo_gen_algorithms import CongruentMethod
from settings.constants import STARTING_POINT, FORMAT_DATA_WITHOUT_MICROSECOND

class Generator:
    
    def set_congruent_method(self, config):
        self._congruent_method = CongruentMethod(
           float(config[self._section_of_config]["SEED"]),
           float(config[self._section_of_config]["A"]),
           float(config[self._section_of_config]["C"]),
           float(config[self._section_of_config]["M"]))

        logging.debug("set congruent method")
           
        

    def next_step(self):
        self._congruent_method.get_next_volume()
        logging.debug("set new step")

    @abstractmethod
    def generate_data(self, range_of_assets):
        pass

class IDGenerator(Generator):

    def __init__(self, config) -> None:
        self._section_of_config = "id_order"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        volume = hex(int(volume))
        
        logging.debug("generate new id: {0}".format(volume))
        return volume

class IDInstrumentGenerator(Generator):

    def __init__(self, config) -> None:
        self._section_of_config = "instrument"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, range_of_assets):
        id_instrument = self._congruent_method.get_current_volume()
        logging.debug("generate new id_instrument: {0}".format(id_instrument))
        return id_instrument

class PxFillGenerator(Generator):

    def __init__(self, config) -> None:
        self._section_of_config = "px_fill"

        self._congruent_method = None
        self.set_congruent_method(config)

        self.__instrument_generator = IDInstrumentGenerator(config)

        self.__comma_wrap = float(config["comma_wrap"]["IN_DIFFERENCE_PX_FILL"])
        self.__count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_PX_FILL"])
        

    def generate_data(self, range_of_assets):
        id_instrument = self.__instrument_generator.generate_data(range_of_assets)
        px_init = JsonGetter.get_volume("instruments", id_instrument, "course")
        px_fill = 0.0
        
        volume = self._congruent_method.get_current_volume()
        difference = volume * self.__comma_wrap

        if difference % 2 == 0:
            px_fill = px_init + difference
        else:
            px_fill = px_init - difference

        px_fill = round(px_fill, self.__count_before_comma)

        logging.debug("genereta new px_fill: {0}".format(px_fill))
        return px_fill

    def next_step(self):
        super().next_step()
        self.__instrument_generator.next_step()

class SideGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "side"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        side = "null"

        if int(volume) % 2 == 0:
            side = JsonGetter.get_volume("sides", 0, "side")
        else:
            side = JsonGetter.get_volume("sides", 1, "side")

        logging.debug("generate new side: {0}".format(side))
        return side

class VolumeInitGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "volume_init"
        
        self._congruent_method = None
        self.set_congruent_method(config)

        self.__comma_wrap = float(config["comma_wrap"]["IN_VOLUME_INIT"])
        self.__count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_VOLUME_INIT"])
    
    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume() * self.__comma_wrap
        volume_init = round(volume, self.__count_before_comma)

        logging.debug("generate new volum_init: {0}".format(volume_init)) 

        return volume_init

class VolumeFillGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "volume_fill"

        self._congruent_method = None
        self.set_congruent_method(config)

        self.__volume_init_generator = VolumeInitGenerator(config)

        self.__comma_wrap = float(config["comma_wrap"]["IN_VOLUME_FILL"]) 
        

    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        difference = volume * self.__comma_wrap

        volume_init = self.__volume_init_generator.generate_data(range_of_assets)
        volume_fill = abs(volume_init - difference)

        if volume_fill > volume_init:
            volume_fill = volume_init
        
        volume_fill = round(volume_fill, 7)
        
        logging.debug("generate new volum_fill: {0}".format(volume_fill)) 

        return volume_fill

    def next_step(self):
        super().next_step()
        self.__volume_init_generator.next_step()

class DateGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "date"

        self._congruent_method = None
        self.set_congruent_method(config)

        self.previos_date = STARTING_POINT
        
    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        dates = []
        for asset in range_of_assets:
            date_in_float = volume + self.previos_date
            
            date_record = datetime.fromtimestamp(date_in_float)
            microsecond = date_record.microsecond
            date = "{}.{}".format(date_record.strftime(FORMAT_DATA_WITHOUT_MICROSECOND), str(microsecond)[:3])
            
            logging.debug("generate new date: {0}".format(date)) 
            dates.append(date)
            self.next_step()
            self.previos_date = date_in_float
        
        
        return dates

class NoteGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "note"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        note = JsonGetter.get_volume("notes", volume, "note")

        logging.debug("generate new note, volume: {0}".format(volume)) 
        return note

class StatusGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "status"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        num_status = None
        
        if volume % 3:
            num_status = 0
        else:
            if volume % 2 == 0:
                num_status = 1
            else:
                num_status = 2

        status = JsonGetter.get_volume("statuses", num_status, "status")
        statuses = ["New", "InProcess", status, "Done"]

        assets_statuses = []

        for status in range_of_assets:
            assets_statuses.append(statuses[status])

        logging.debug("generate new statuses, volume: {0}, statuses {1}".format(volume, assets_statuses)) 
        
        return assets_statuses
    
class TagsGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "array_tag"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, range_of_assets):
        volume = self._congruent_method.get_current_volume()
        count_of_tags = JsonGetter.get_count_of_name_array("tags")
        tags = ""

        for tag in range(count_of_tags):
            if volume % 2 == 0:
                tags += JsonGetter.get_volume("tags", tag, "tag") + " "

            self.next_step()
        
        return tags

class GeneratorAssetStrategy:
    def __init__(self, range_of_asset, count_assets, config) -> None:
        self.__range_of_asset = range_of_asset
        self.__count_assets = count_assets
        self.__generators = [
            IDGenerator(config),
            IDInstrumentGenerator(config),
            PxFillGenerator(config),
            SideGenerator(config),
            VolumeInitGenerator(config),
            VolumeFillGenerator(config),
            DateGenerator(config),
            StatusGenerator(config),
            NoteGenerator(config),
            TagsGenerator(config)
        ]    

    @property
    def count_assets(self):
        return self.__count_assets

    def generate_asset(self):
        if self.__generators == None:
            logging.error("generators have not been initialized!!!")
            return

        record = []

        for generator in self.__generators:
            record.append(generator.generate_data(self.__range_of_asset))
            generator.next_step()

        asset = DTOAsset()

        asset.id_order = record[0]
        asset.quotation = JsonGetter.get_volume("instruments", record[1], "quotation")
        asset.px_init = JsonGetter.get_volume("instruments", record[1], "course")
        asset.px_fill = record[2]
        asset.side = record[3]
        asset.volume_init = record[4]
        asset.volume_fill = record[5]
        asset.date = record[6]
        asset.status = record[7]
        asset.note = record[8]
        asset.tags = record[9]

        return asset

        