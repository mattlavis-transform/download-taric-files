import classes.globals as g


class MeursingAdditionalCode(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        meursing_additional_code_sid = g.app.get_number_value(message, ".//oub:meursing.additional.code.sid", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "Meursing additional code", additional_code)

