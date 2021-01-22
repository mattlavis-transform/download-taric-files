from datetime import datetime
import classes.globals as g


class FootnoteAssociationGoodsNomenclature(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        goods_nomenclature_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.sid", True)
        footnote_type = g.app.get_value(message, ".//oub:footnote.type", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        code = footnote_type + footnote_id
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        productline_suffix = g.app.get_value(message, ".//oub:productline.suffix", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote association goods nomenclature", goods_nomenclature_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):
                if validity_end_date is None:
                    validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
                else:
                    validity_end_date2 = validity_end_date
                # Business rule FO6
                sql = """select validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD'))
                from footnotes where footnote_type_id = %s and footnote_id = %s limit 1"""
                params = [
                    footnote_type,
                    footnote_id
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) == 1:
                    footnote_start_date = rows[0][0]
                    footnote_end_date = rows[0][1]
                    if (footnote_start_date > validity_start_date) or (validity_end_date2 > footnote_end_date):
                        g.data_file.record_business_rule_violation("FO6", "When a footnote is used in a goods nomenclature the validity period "
                        "of the footnote must span the validity period of the association with the goods nomenclature.",
                        operation, transaction_id, message_id, record_code, sub_record_code, code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnote_association_goods_nomenclatures_oplog (goods_nomenclature_sid,
            footnote_type, footnote_id, validity_start_date, validity_end_date,
            goods_nomenclature_item_id, productline_suffix,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (goods_nomenclature_sid,
            footnote_type, footnote_id, validity_start_date, validity_end_date,
            goods_nomenclature_item_id, productline_suffix,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, goods_nomenclature_item_id)
        cur.close()
