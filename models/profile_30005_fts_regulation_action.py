import classes.globals as g


class FtsRegulationAction(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        fts_regulation_role = g.app.get_value(message, ".//oub:fts.regulation.role", True)
        fts_regulation_id = g.app.get_value(message, ".//oub:fts.regulation.id", True)
        stopped_regulation_role = g.app.get_value(message, ".//oub:stopped.regulation.role", True)
        stopped_regulation_id = g.app.get_value(message, ".//oub:stopped.regulation.id", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "certifiFTS regulation action", fts_regulation_id)

