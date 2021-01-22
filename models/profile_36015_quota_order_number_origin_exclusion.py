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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type == "1":
                # Business rule ON13	An exclusion can only be entered if the order number origin is a geographical area group (area code = 1).
                geographical_area = g.app.get_geographical_area_from_origin(quota_order_number_origin_sid)
                if len(geographical_area) > 0:
                    geo_validity_start_date = geographical_area[0]
                    geo_validity_end_date = geographical_area[1]
                    geo_area_code = geographical_area[3]
                    if geo_area_code != "1":
                        g.data_file.record_business_rule_violation("ON13", "An exclusion can only be entered if the order number origin is a "
                        "geographical area group (area code = 1).", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_origin_sid)

            # DBFK Check the origin exists
            sql = "select quota_order_number_origin_sid from quota_order_number_origins where quota_order_number_origin_sid = %s"
            params = [
                str(quota_order_number_origin_sid)
            ]
            cur = g.app.conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            if len(rows) == 0:
                g.data_file.record_business_rule_violation("DBFK", "The referenced quota order number origin must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_order_number_origin_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO quota_order_number_origin_exclusions_oplog (quota_order_number_origin_sid, excluded_geographical_area_sid, operation, operation_date)
            VALUES (%s, %s, %s, %s)""",
            (quota_order_number_origin_sid, excluded_geographical_area_sid, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_origin_sid)
        cur.close()
