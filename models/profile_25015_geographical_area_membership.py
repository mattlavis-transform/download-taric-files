from datetime import datetime
import classes.globals as g


class GeographicalAreaMembership(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        geographical_area_group_sid = g.app.get_number_value(message, ".//oub:geographical.area.group.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "geographical area membership", geographical_area_group_sid)

