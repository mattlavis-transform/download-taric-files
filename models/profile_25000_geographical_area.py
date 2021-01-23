from datetime import datetime
import classes.globals as g


class GeographicalArea(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        geographical_area_id = g.app.get_value(message, ".//oub:geographical.area.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        geographical_code = g.app.get_value(message, ".//oub:geographical.code", True)
        parent_geographical_area_group_sid = g.app.get_number_value(message, ".//oub:parent.geographical.area.group.sid", True)
        validity_start_date_string = validity_start_date.strftime('%Y-%m-%d')
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

        geographical_area_groups = g.app.get_geographical_area_groups()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "geographical area", geographical_area_id)

