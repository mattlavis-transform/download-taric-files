import sys
import classes.globals as g


class RegulationGroup(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        regulation_group_id = g.app.get_value(message, ".//oub:regulation.group.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        regulation_groups = g.app.get_regulation_groups()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "regulation group", regulation_group_id)

