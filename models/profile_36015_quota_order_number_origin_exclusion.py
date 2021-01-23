from datetime import datetime
import classes.globals as g


class QuotaOrderNumberOriginExclusion(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_order_number_origin_sid = g.app.get_number_value(message, ".//oub:quota.order.number.origin.sid", True)
        excluded_geographical_area_sid = g.app.get_number_value(message, ".//oub:excluded.geographical.area.sid", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota order number origin exclusion", quota_order_number_origin_sid)

