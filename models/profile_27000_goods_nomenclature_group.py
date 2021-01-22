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

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO goods_nomenclature_groups_oplog (goods_nomenclature_group_type, goods_nomenclature_group_id,
            validity_start_date, validity_end_date, nomenclature_group_facility_code,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (goods_nomenclature_group_type, goods_nomenclature_group_id,
            validity_start_date, validity_end_date, nomenclature_group_facility_code,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, goods_nomenclature_group_id)
        cur.close()
