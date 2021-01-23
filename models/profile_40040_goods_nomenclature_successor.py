import classes.globals as g


class GoodsNomenclatureSuccessor(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        goods_nomenclature_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.sid", True)
        absorbed_goods_nomenclature_item_id = g.app.get_value(message, ".//oub:absorbed.goods.nomenclature.item.id", True)
        absorbed_productline_suffix = g.app.get_value(message, ".//oub:absorbed.productline.suffix", True)
        goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        productline_suffix = g.app.get_value(message, ".//oub:productline.suffix", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "goods nomenclature successor", goods_nomenclature_sid)

