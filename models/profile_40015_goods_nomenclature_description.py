import classes.globals as g
from classes.database import Database

import sys


class GoodsNomenclatureDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        self.goods_nomenclature_description_periods = []
        self.matched = False
        self.operation_date = g.app.get_timestamp()
        self.goods_nomenclature_description_period_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.description.period.sid", True)
        self.language_id = g.app.get_value(message, ".//oub:language.id", True)
        self.goods_nomenclature_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.sid", True)
        self.goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        self.productline_suffix = g.app.get_value(message, ".//oub:productline.suffix", True)
        self.description = g.app.get_value(message, ".//oub:description", True)
        # Set operation types and print load message to screen
        self.operation = g.app.get_loading_message(update_type, "goods nomenclature description for period", self.goods_nomenclature_description_period_sid)

    def lookup_start_date(self):
        self.validity_start_date = ""
        sql = "select validity_start_date from goods_nomenclature_description_periods where goods_nomenclature_description_period_sid = " + str(self.goods_nomenclature_description_period_sid)
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            self.validity_start_date = str(row[0])
