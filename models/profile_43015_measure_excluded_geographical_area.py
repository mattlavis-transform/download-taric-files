import sys
import classes.globals as g


class MeasureExcludedGeographicalArea(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        excluded_geographical_area = g.app.get_value(message, ".//oub:excluded.geographical.area", True)
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "excluded_geographical_area on measure_sid", str(measure_sid) + "/" + excluded_geographical_area)

