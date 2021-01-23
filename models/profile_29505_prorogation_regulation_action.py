import classes.globals as g


class ProrogationRegulationAction(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        prorogation_regulation_role = g.app.get_value(message, ".//oub:prorogation.regulation.role", True)
        prorogation_regulation_id = g.app.get_value(message, ".//oub:prorogation.regulation.id", True)
        prorogated_regulation_role = g.app.get_value(message, ".//oub:prorogated.regulation.role", True)
        prorogated_regulation_id = g.app.get_value(message, ".//oub:prorogated.regulation.id", True)
        prorogated_date = g.app.get_date_value(message, ".//oub:prorogated.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "prorogation regulation action", prorogation_regulation_id)

