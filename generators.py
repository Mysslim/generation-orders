import logging
from abc import abstractmethod
from datetime import datetime
from json_getter import JsonGetter
from pseudo_gen_algorithms import CongruentMethod
from settings.constants import STARTING_POINT, FORMAT_DATA_WITHOUT_MICROSECOND, COUNT_STARTED_ORDERS, COUNT_FULL_ORDERS, COUNT_UNFINISH_ORDERS

class Generator:
    
    def set_congruent_method(self, config):
       self._congruent_method = CongruentMethod(
           float(config[self._section_of_config]["SEED"]),
           float(config[self._section_of_config]["A"]),
           float(config[self._section_of_config]["C"]),
           float(config[self._section_of_config]["M"]))

    def next_step(self):
        self._congruent_method.get_next_volume()

    @abstractmethod
    def generate_data(self, num_result):
        pass

class IDGenerator(Generator):

    def __init__(self, config) -> None:
        self._section_of_config = "id_order"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, num_result):
        volume = self._congruent_method.get_current_volume()
        volume = hex(int(volume))
        
        logging.debug("generate new id: {0}".format(volume))
        return volume

class IDInstrumentGenerator(Generator):

    def __init__(self, config) -> None:
        self._section_of_config = "instrument"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, num_result):
        return self._congruent_method.get_current_volume()

class QuotationGenerator(Generator):

    def __init__(self, config) -> None:
        self.__idinstrument_generator = IDInstrumentGenerator(config)

    def generate_data(self, num_result):
        id_instrument = self.__idinstrument_generator.generate_data(num_result)
        return JsonGetter.get_volume("instruments", id_instrument, "quotation")

    def next_step(self):
        self.__idinstrument_generator.next_step()

class PxInitGenerator(Generator):
    def __init__(self, config) -> None:
        self.__idinstrument_generator = IDInstrumentGenerator(config)

    def generate_data(self, num_result):
        id_instrument = self.__idinstrument_generator.generate_data(num_result)
        return JsonGetter.get_volume("instruments", id_instrument, "course")

    def next_step(self):
        self.__idinstrument_generator.next_step()

class PxFillGenerator(Generator):

    def __init__(self, config) -> None:
        self._section_of_config = "px_fill"

        self._congruent_method = None
        self.set_congruent_method(config)

        self.__instrument_generator = IDInstrumentGenerator(config)

        self.__comma_wrap = float(config["comma_wrap"]["IN_DIFFERENCE_PX_FILL"])
        self.__count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_PX_FILL"])
        

    def generate_data(self, num_result):
        id_instrument = self.__instrument_generator.generate_data(num_result)
        px_init = JsonGetter.get_volume("instruments", id_instrument, "course")
        px_fill = 0.0
        
        volume = self._congruent_method.get_current_volume()
        difference = volume * self.__comma_wrap

        if difference % 2 == 0:
            px_fill = px_init + difference
        else:
            px_fill = px_init - difference

        px_fill = round(px_fill, self.__count_before_comma)
        return px_fill

    def next_step(self):
        super().next_step()
        self.__instrument_generator.next_step()

class SideGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "side"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, num_result):
        volume = self._congruent_method.get_current_volume()
        side = "null"

        if int(volume) % 2 == 0:
            side = JsonGetter.get_volume("sides", 0, "side")
        else:
            side = JsonGetter.get_volume("sides", 1, "side")

        return side

class VolumeInitGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "volume_init"
        
        self._congruent_method = None
        self.set_congruent_method(config)

        self.__comma_wrap = float(config["comma_wrap"]["IN_VOLUME_INIT"])
        self.__count_before_comma = int(config["comma_wrap"]["COUNT_BEFORE_COMMA_FOR_VOLUME_INIT"])
    
    def generate_data(self, num_result):
        volume = self._congruent_method.get_current_volume() * self.__comma_wrap
        volume_init = round(volume, self.__count_before_comma)

        return volume_init

class VolumeFillGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "volume_fill"

        self._congruent_method = None
        self.set_congruent_method(config)

        self.__volume_init_generator = VolumeInitGenerator(config)
        self.__status_generator = StatusGenerator(config)

        self.__comma_wrap = float(config["comma_wrap"]["IN_VOLUME_FILL"]) 
        

    def generate_data(self, num_result):
        status = self.__status_generator.generate_data(num_result)

        if status != "Fill" and status != "ParticalFill":
            return 0
        
        volume = self._congruent_method.get_current_volume()
        difference = volume * self.__comma_wrap

        volume_init = self.__volume_init_generator.generate_data(num_result)
        volume_fill = abs(volume_init - difference)

        if volume_fill > volume_init:
            volume_fill = volume_init
        
        volume_fill = round(volume_fill, 7)
        
        return volume_fill

    def next_step(self):
        super().next_step()
        self.__volume_init_generator.next_step()
        self.__status_generator.next_step()

class DateGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "date"

        self._congruent_method = None
        self.set_congruent_method(config)

        self.previos_date = STARTING_POINT
        
    def generate_data(self, num_result):
        volume = self._congruent_method.get_current_volume()

        date_in_float = volume + self.previos_date
        date_record = datetime.fromtimestamp(date_in_float)
        microsecond = date_record.microsecond
        date = "{}.{}".format(date_record.strftime(FORMAT_DATA_WITHOUT_MICROSECOND), str(microsecond)[:3])
        
        self.next_step()
        self.previos_date = date_in_float
        return date

class NoteGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "note"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, num_result):
        volume = self._congruent_method.get_current_volume()
        note = JsonGetter.get_volume("notes", volume, "note")
        return note

class StatusGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "status"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, num_result):
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
        
        return statuses[num_result]
    
class TagsGenerator(Generator):
    def __init__(self, config) -> None:
        self._section_of_config = "array_tag"

        self._congruent_method = None
        self.set_congruent_method(config)

    def generate_data(self, num_result):
        volume = self._congruent_method.get_current_volume()
        count_of_tags = JsonGetter.get_count_of_name_array("tags")
        tags = ""

        for tag in range(count_of_tags):
            if volume % 2 == 0:
                tags += JsonGetter.get_volume("tags", tag, "tag") + " "

            self.next_step()
        
        return tags

class GeneratorHistoryRecord:
    def __init__(self, config) -> None:
        self.__generated_record = []
        self.__generators = GeneratorBuilder.get_generators(config)

    def get_generated_record(self):
        return self.__generated_record

    def __generate_orders(self, count_orders, range_for_statuses):
        if self.__generators == None:
            logging.error("generators have not been initialized!!!")
            return

        for order in range(count_orders):
            for status in range_for_statuses:
                record = []

                for generator in self.__generators:
                    record.append(generator.generate_data(status))
                
                print(record)
                self.__generated_record.append(record)
            
            for generator in self.__generators:
                    generator.next_step()
    
    def already_open_orders(self):
        self.__generate_orders(COUNT_STARTED_ORDERS, range(3))

    def completed_orders(self):
        self.__generate_orders(COUNT_FULL_ORDERS, range(4))

    def unfinished_orders(self):
        self.__generate_orders(COUNT_UNFINISH_ORDERS, range(1, 4))

class GeneratorBuilder:
    def get_generators(self, config):
        return [
            IDGenerator(config),
            QuotationGenerator(config),
            PxInitGenerator(config),
            PxFillGenerator(config),
            SideGenerator(config),
            VolumeInitGenerator(config),
            VolumeFillGenerator(config),
            DateGenerator(config),
            StatusGenerator(config),
            NoteGenerator(config),
            TagsGenerator(config)
        ]    


        