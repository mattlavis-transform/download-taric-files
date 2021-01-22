from datetime import datetime
import classes.globals as g


class GoodsNomenclature(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        goods_nomenclature_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.sid", True)
        goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        producline_suffix = g.app.get_value(message, ".//oub:producline.suffix", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        statistical_indicator = g.app.get_value(message, ".//oub:statistical.indicator", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "goods nomenclature", goods_nomenclature_sid)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO goods_nomenclatures_oplog (goods_nomenclature_sid,
            goods_nomenclature_item_id, producline_suffix,
            validity_start_date, validity_end_date, statistical_indicator, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (goods_nomenclature_sid,
            goods_nomenclature_item_id, producline_suffix,
            validity_start_date, validity_end_date, statistical_indicator, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, goods_nomenclature_item_id)
        cur.close()

        g.app.goods_nomenclatures = g.app.get_all_goods_nomenclatures()
