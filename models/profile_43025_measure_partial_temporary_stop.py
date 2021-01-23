import classes.globals as g


class MeasurePartialTemporaryStop(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        partial_temporary_stop_regulation_id = g.app.get_value(message, ".//oub:partial.temporary.stop.regulation.id", True)
        partial_temporary_stop_regulation_officialjournal_number = g.app.get_value(message, ".//oub:partial.temporary.stop.regulation.officialjournal.number", True)
        partial_temporary_stop_regulation_officialjournal_page = g.app.get_value(message, ".//oub:partial.temporary.stop.regulation.officialjournal.page", True)
        abrogation_regulation_id = g.app.get_value(message, ".//oub:abrogation.regulation.id", True)
        abrogation_regulation_officialjournal_number = g.app.get_value(message, ".//oub:abrogation.regulation.officialjournal.number", True)
        abrogation_regulation_officialjournal_page = g.app.get_value(message, ".//oub:abrogation.regulation.officialjournal.page", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "partial temporary stop on measure_sid", measure_sid)

