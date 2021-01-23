import sys
import classes.globals as g


class GoodsNomenclatureGroup(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        goods_nomenclature_group_type = g.app.get_value(message, ".//oub:goods.nomenclature.group.type", True)
        goods_nomenclature_group_id = g.app.get_value(message, ".//oub:goods.nomenclature.group.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        nomenclature_group_facility_code = g.app.get_value(message, ".//oub:nomenclature.group.facility.code", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "goods nomenclature group", goods_nomenclature_group_id)

