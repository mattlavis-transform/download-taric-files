import classes.globals as g


class ExportRefundNomenclatureIndent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        export_refund_nomenclature_indents_sid = g.app.get_number_value(message, ".//oub:export.refund.nomenclature.indents.sid", True)
        export_refund_nomenclature_sid = g.app.get_number_value(message, ".//oub:export.refund.nomenclature.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        number_export_refund_nomenclature_indents = g.app.get_number_value(message, ".//oub:number.export.refund.nomenclature.indents", True)
        goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        additional_code_type = g.app.get_value(message, ".//oub:additional.code.type", True)
        export_refund_code = g.app.get_value(message, ".//oub:export.refund.code", True)
        productline_suffix = g.app.get_value(message, ".//oub:productline.suffix", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "export refund nomenclature indent", export_refund_nomenclature_indents_sid)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO export_refund_nomenclature_indents_oplog (export_refund_nomenclature_indents_sid,
            export_refund_nomenclature_sid, validity_start_date, number_export_refund_nomenclature_indents,
            goods_nomenclature_item_id, additional_code_type, export_refund_code, productline_suffix,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (export_refund_nomenclature_indents_sid,
            export_refund_nomenclature_sid, validity_start_date, number_export_refund_nomenclature_indents,
            goods_nomenclature_item_id, additional_code_type, export_refund_code, productline_suffix,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, export_refund_nomenclature_indents_sid)
        cur.close()
