import classes.globals as g


class AdditionalCode(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_sid = g.app.get_number_value(message, ".//oub:additional.code.sid", True)
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code//oub:additional.code", True)
        code = additional_code_type_id + additional_code
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "additional code", code)

