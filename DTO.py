import logging
from os import stat
from json_getter import JsonGetter

class DTORecord:
    def __init__(
        self, 
        id_order = "none", 
        quotation = "none",
        px_init = 0.0,
        px_fill = 0.0,
        volume_init = 0.0,
        volume_fill = 0.0,
        side = "none",
        date = "none",
        status = "none",
        note = "none",
        tags = "none"
        ) -> None:

        self.id_order = id_order
        self.quotation = quotation
        self.px_init = px_init
        self.px_fill = px_fill
        self.volume_init = volume_init 
        self.volume_fill = volume_fill
        self.side = side
        self.date = date
        self.status = status
        self.note = note
        self.tags = tags

        @property
        def id_order(self):
            return self.id_order

        @id_order.setter
        def id_order(self, id_order):
            self.id_order = id_order

        @property
        def quotation(self):
            return self.quotation

        @quotation.setter
        def quotation(self, id_instrument):
            self.quotation = JsonGetter.get_volume("instrument", id_instrument, "quotation")

        @property
        def px_init(self):
            return self.px_init

        @px_init.setter
        def px_init(self, id_instrument):
            self.px_init = JsonGetter.get_volume("instrument", id_instrument, "course")

        @property
        def px_fill(self):
            return self.px_fill

        @px_fill.setter
        def px_fill(self, px_fill):
            self.px_fill = px_fill

        @property
        def volume_init(self):
            return self.volume_init

        @volume_init.setter
        def volume_init(self, volume_init):
            self.volume_init = volume_init

        @property
        def volume_fill(self):
            return self.volume_fill

        @volume_fill.setter
        def volume_fill(self, volume_fill):
            if self.status == "none":
                logging.error("you need initialize status before volume_fill!!!")
                return

            if self.status == "Fill" or self.status == "ParticalFill":
                self.volume_fill = volume_fill
            else:
                self.volume_fill = 0

        @property
        def side(self):
            return self.side

        @side.setter
        def side(self, side):
            self.side = side

        @property
        def date(self):
            return self.date

        @date.setter
        def date(self, date):
            self.date = date
 
        @property
        def status(self):
            return self.status

        @status.setter
        def status(self, status):
            self.status = status

        @property
        def note(self):
            return self.note

        @note.setter
        def note(self, note):
            self.note = note

        @property
        def tags(self):
            return self.tags

        @tags.setter
        def tags(self, tags):
            self.tags = tags

class DTOAsset():
    def __init__(
        self, 
        id_order = "none", 
        quotation = "none",
        px_init = 0.0,
        px_fill = 0.0,
        volume_init = 0.0,
        volume_fill = 0.0,
        side = "none",
        date = "none",
        status = "none",
        note = "none",
        tags = "none"
        ) -> None:

        self.id_order = id_order
        self.quotation = quotation
        self.px_init = px_init
        self.px_fill = px_fill
        self.volume_init = volume_init 
        self.volume_fill = volume_fill
        self.side = side
        self.date = date
        self.status = status
        self.note = note
        self.tags = tags

        @property
        def id_order(self):
            return self.id_order

        @id_order.setter
        def id_order(self, id_order):
            self.id_order = id_order

        @property
        def quotation(self):
            return self.quotation

        @quotation.setter
        def quotation(self, id_instrument):
            self.quotation = JsonGetter.get_volume("instrument", id_instrument, "quotation")

        @property
        def px_init(self):
            return self.px_init

        @px_init.setter
        def px_init(self, id_instrument):
            self.px_init = JsonGetter.get_volume("instrument", id_instrument, "course")

        @property
        def px_fill(self):
            return self.px_fill

        @px_fill.setter
        def px_fill(self, px_fill):
            self.px_fill = px_fill

        @property
        def volume_init(self):
            return self.volume_init

        @volume_init.setter
        def volume_init(self, volume_init):
            self.volume_init = volume_init

        @property
        def volume_fill(self):
            return self.volume_fill

        @volume_fill.setter
        def volume_fill(self, volume_fill):
            self.volume_fill = volume_fill

        @property
        def side(self):
            return self.side

        @side.setter
        def side(self, side):
            self.side = side

        @property
        def date(self):
            return self.date

        @date.setter
        def date(self, date):
            self.date = date
 
        @property
        def status(self):
            return self.status

        @status.setter
        def status(self, status):
            self.status = status

        @property
        def note(self):
            return self.note

        @note.setter
        def note(self, note):
            self.note = note

        @property
        def tags(self):
            return self.tags

        @tags.setter
        def tags(self, tags):
            self.tags = tags