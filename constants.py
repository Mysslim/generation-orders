STARTING_POINT = 1613643729.758686 # start point the date

COUNT_ORDERS = 2000

COUNT_RECORDS = 7200

COUNT_COMBINATION_OF_TAGS = 60

COUNT_STARTED_ORDERS = 600

COUNT_FULL_ORDERS = 1200

COUNT_UNFINISH_ORDERS = 200

FORMAT_DATA_WITHOUT_MICROSECOND = "%d.%m.%Y %H:%M:%S"

FORMAT_FOR_LOGGER = "%(asctime)s-%(levelname)s-%(message)s"

INSTRUMENTS = [
    ["EUR/RUB", 92.018],
    ["EUR/USD", 1.238],
    ["EUR/JPY", 127.1],
    ["USD/RUB", 75.955],
    ["USD/UAH", 28.159],
    ["GBP/UAH", 38.594],
    ["USD/CHF", 0.891],
    ["JPY/USD", 0.0096],
    ["GBP/USD", 1.2212],
    ["NZD/USD", 0.7184],
    ["USD/JPY", 104.7]
]

TAGS = [
    "fast",
    "dealing",
    "value",
    "USD",
    "course",
    "1$ = 5₴",
    "finance",
    "EUR",
    "UAH",
    "score",
    "quickly",
]

NOTES = [
    "this text is 1 note, some text to make the note look long",
    "this text is 2 note, some text to make the note look long",
    "this text is 3 note, some text to make the note look long",
    "this text is 4 note, some text to make the note look long",
    "this text is 5 note, some text to make the note look long",
    "this text is 6 note, some text to make the note look long",
    "this text is 7 note, some text to make the note look long",
    "this text is 8 note, some text to make the note look long",
    "this text is 9 note, some text to make the note look long",
    "this text is 10 note, some text to make the note look long",
    "this text is 11 note, some text to make the note look long"
]

SIDES = [
    "Buy",
    "Sell"
]

STATUSES = [
    "New",
    "InProcess",
    "Fill",
    "ParticalFill",
    "Cancel",
    "Done"
]

TEMPLATE_FOR_STATUS = {
        COUNT_STARTED_ORDERS: [STATUSES[1], STATUSES[2], STATUSES[5]],
        COUNT_FULL_ORDERS: [STATUSES[0], STATUSES[1], STATUSES[2], STATUSES[5]],
        COUNT_UNFINISH_ORDERS : [STATUSES[0], STATUSES[1], STATUSES[2]]
    }