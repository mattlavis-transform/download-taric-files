import classes.globals as g


class QuotaCriticalEvent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_definition_sid = g.app.get_number_value(message, ".//oub:quota.definition.sid", True)
        occurrence_timestamp = g.app.get_date_value(message, ".//oub:occurrence.timestamp", True)
        critical_state = g.app.get_value(message, ".//oub:critical.state", True)
        critical_state_change_date = g.app.get_date_value(message, ".//oub:critical.state.change.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota critical event for quota definition", quota_definition_sid)

