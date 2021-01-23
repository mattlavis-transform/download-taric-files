import classes.globals as g


class QuotaClosedAndBalanceTransferredEvent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_definition_sid = g.app.get_number_value(message, ".//oub:quota.definition.sid", True)
        occurrence_timestamp = g.app.get_value(message, ".//oub:occurrence.timestamp", True)
        closing_date = g.app.get_date_value(message, ".//oub:closing.date", True)
        transferred_amount = g.app.get_number_value(message, ".//oub:transferred.amount", True)
        target_quota_definition_sid = g.app.get_number_value(message, ".//oub:target.quota.definition.sid", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota closed and balance transferred event for quota definition", quota_definition_sid)

