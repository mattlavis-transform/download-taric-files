import classes.globals as g


class ExportRefundNomenclatureDescriptionPeriod(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        export_refund_nomenclature_description_period_sid = g.app.get_number_value(message, ".//oub:export.refund.nomenclature.description.period.sid", True)
        export_refund_nomenclature_sid = g.app.get_number_value(message, ".//oub:export.refund.nomenclature.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        additional_code_type = g.app.get_value(message, ".//oub:additional.code.type", True)
        export_refund_code = g.app.get_value(message, ".//oub:export.refund.code", True)
        productline_suffix = g.app.get_value(message, ".//oub:productline.suffix", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "export refund nomenclature description period", export_refund_nomenclature_description_period_sid)

