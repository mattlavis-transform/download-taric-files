import classes.globals as g


class FootnoteAssociationAdditionalCode(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_sid = g.app.get_number_value(message, ".//oub:additional.code.sid", True)
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote association on additional code", additional_code_sid)

