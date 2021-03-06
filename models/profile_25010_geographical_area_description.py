import classes.globals as g


class GeographicalAreaDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        geographical_area_description_period_sid = g.app.get_number_value(message, ".//oub:geographical.area.description.period.sid", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        geographical_area_id = g.app.get_value(message, ".//oub:geographical.area.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "geographical area description", geographical_area_id)

