import classes.globals as g


class GeographicalAreaDescriptionPeriod(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        geographical_area_description_period_sid = g.app.get_number_value(message, ".//oub:geographical.area.description.period.sid", True)
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        geographical_area_id = g.app.get_value(message, ".//oub:geographical.area.id", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "geographical area description period", geographical_area_description_period_sid)

