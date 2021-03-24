from pymysql import connect
from DTO import *

class MappingAssetInRecord:
    def __init__(self, config) -> None:
        self.config = config
    def get_records_from_asset(asset: DTOAsset):
        records = []

        for record in range(len(asset.status)):
            dto_record = DTORecord(
                asset.id_order,
                asset.quotation,
                asset.px_init,
                asset.px_fill,
                asset.volume_init,
                asset.volume_fill,
                asset.side,
                asset.date[record],
                asset.status[record],
                asset.note,
                asset.tags
            )

            if asset.status[record] != "Fill" and asset.status[record] != "ParcitalFill":
                dto_record.volume_fill = 0
                dto_record.px_fill = 0

            records.append(dto_record)
        
        return records