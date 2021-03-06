from datetime import datetime
import classes.globals as g


class QuotaOrderNumber(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_order_number_sid = g.app.get_number_value(message, ".//oub:quota.order.number.sid", True)
        quota_order_number_id = g.app.get_value(message, ".//oub:quota.order.number.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota order number", quota_order_number_id)

