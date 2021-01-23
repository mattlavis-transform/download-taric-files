import sys
import classes.globals as g


class GoodsNomenclatureGroupDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        goods_nomenclature_group_type = g.app.get_value(message, ".//oub:goods.nomenclature.group.type", True)
        goods_nomenclature_group_id = g.app.get_value(message, ".//oub:goods.nomenclature.group.id", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "goods nomenclature group description", goods_nomenclature_group_id)

