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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            quota_order_numbers = g.app.get_quota_order_numbers()

            # Business rule ON3 The start date must be less than or equal to the end date.
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("ON3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)

            if update_type == "3":  # INSERT
                for qon in g.app.quota_order_numbers:
                    quota_order_number_id2 = qon[0]
                    quota_order_number_sid2 = qon[1]
                    validity_start_date2 = qon[2]
                    validity_end_date2 = qon[3]

                    # Business rule ON1 Quota order number id + start date must be unique.
                    if quota_order_number_id == quota_order_number_id2 and validity_start_date == validity_start_date2:
                        g.data_file.record_business_rule_violation("ON1", "Quota order number id + start date must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
                        break

                    # Business rule DBFK
                    if quota_order_number_sid == quota_order_number_sid2:
                        g.data_file.record_business_rule_violation("DBFK", "Quota order number sid already exists.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
                        break

                    if quota_order_number_id == quota_order_number_id2:
                        if validity_end_date is None:
                            if validity_end_date2 is not None:
                                if validity_start_date <= validity_end_date2:
                                    g.data_file.record_business_rule_violation("ON2(a)", "There may be no overlap in time of two quota order numbers with the same quota order number id.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
                                    break
                            else:
                                g.data_file.record_business_rule_violation("ON2(b)", "There may be no overlap in time of two quota order numbers with the same quota order number id.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
                                break
                        else:
                            if validity_end_date2 is not None:
                                if (validity_start_date <= validity_end_date2 and validity_end_date >= validity_start_date2):
                                    g.data_file.record_business_rule_violation("ON2(c)", "There may be no overlap in time of two quota order numbers with the same quota order number id.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
                                    break
                            else:
                                g.data_file.record_business_rule_violation("ON2(d)", "There may be no overlap in time of two quota order numbers with the same quota order number id.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
                                break

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO quota_order_numbers_oplog (quota_order_number_sid,
            quota_order_number_id, validity_start_date, validity_end_date, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (quota_order_number_sid, quota_order_number_id, validity_start_date, validity_end_date, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_id)
        cur.close()

        quota_order_numbers = g.app.get_quota_order_numbers()
