import classes.globals as g


class QuotaSuspensionPeriod(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_suspension_period_sid = g.app.get_number_value(message, ".//oub:quota.suspension.period.sid", True)
        quota_definition_sid = g.app.get_number_value(message, ".//oub:quota.definition.sid", True)
        suspension_start_date = g.app.get_date_value(message, ".//oub:suspension.start.date", True)
        suspension_end_date = g.app.get_date_value(message, ".//oub:suspension.end.date", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota suspension period", quota_suspension_period_sid)

