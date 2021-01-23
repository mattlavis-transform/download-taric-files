from datetime import datetime
import classes.globals as g


class QuotaOrderNumberOrigin(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_order_number_origin_sid = g.app.get_number_value(message, ".//oub:quota.order.number.origin.sid", True)
        quota_order_number_sid = g.app.get_number_value(message, ".//oub:quota.order.number.sid", True)
        geographical_area_id = g.app.get_value(message, ".//oub:geographical.area.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota order number origin", str(quota_order_number_sid) + " / " + geographical_area_id)

