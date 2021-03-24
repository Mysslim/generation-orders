from generators import GeneratorAssetStrategy
from mapping import MappingAssetInRecord
from settings.constants import COUNT_STARTED_ORDERS, COUNT_FULL_ORDERS, COUNT_UNFINISH_ORDERS


class BuilderGeneratorAsset:
    def __init__(self, config) -> None:
        self.__strategies = [
            GeneratorAssetStrategy(range(3), COUNT_STARTED_ORDERS, config),
            GeneratorAssetStrategy(range(4), COUNT_FULL_ORDERS, config),
            GeneratorAssetStrategy(range(1, 4), COUNT_UNFINISH_ORDERS, config)
        ]

    def get_count_strategies(self):
        return len(self.__strategies)

    def get_count_assets(self, index_of_generator: int):
        return self.__strategies[index_of_generator].count_assets

    def get_records(self, index_of_generator: int):
        asset = self.__strategies[index_of_generator].generate_asset()
        records = MappingAssetInRecord.get_records_from_asset(asset)

        return records
