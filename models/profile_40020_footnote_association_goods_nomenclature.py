from datetime import datetime
import classes.globals as g


class FootnoteAssociationGoodsNomenclature(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        self.operation_date = g.app.get_timestamp()
        self.goods_nomenclature_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.sid", True)
        self.footnote_type = g.app.get_value(message, ".//oub:footnote.type", True)
        self.footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        self.code = self.footnote_type + self.footnote_id
        self.validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        self.validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        self.goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        self.productline_suffix = g.app.get_value(message, ".//oub:productline.suffix", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote association goods nomenclature", self.goods_nomenclature_sid)

