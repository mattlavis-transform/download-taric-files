import classes.globals as g


class AdditionalCodeDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_description_period_sid = g.app.get_number_value(message, ".//oub:additional.code.description.period.sid", True)
        additional_code_sid = g.app.get_number_value(message, ".//oub:additional.code.sid", True)
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code", True)
        code = additional_code_type_id + additional_code
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "additional code description", additional_code_type_id + additional_code + " (" + description + ")")

