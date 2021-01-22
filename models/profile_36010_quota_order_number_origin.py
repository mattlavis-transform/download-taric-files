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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            # Business rule ON4
            if geographical_area_sid not in g.app.geographical_area_sids:
                g.data_file.record_business_rule_violation("ON4(a)", "The referenced geographical area must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_order_number_sid))

            # Business rule ON4 (on SIDs)
            if geographical_area_id not in g.app.geographical_areas:
                g.data_file.record_business_rule_violation("ON4(b)", "The referenced geographical area must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_order_number_sid))

            if update_type == "3":
                # Business rule ON5	There may be no overlap in time of two quota order number origins with the same quota order number SID and geographical area id.
                existing_related_origins = g.app.get_existing_related_origins(quota_order_number_sid, geographical_area_id)
                if len(existing_related_origins) > 0:
                    for row in existing_related_origins:
                        existing_start_date = row[1]
                        existing_end_date = row[2]
                        # (StartDate1 <= EndDate2) and (StartDate2 <= EndDate1)
                        if (existing_start_date <= validity_end_date2) and (validity_start_date <= existing_end_date):
                            g.data_file.record_business_rule_violation("ON5", "There may be no overlap in time of two quota order number origins with the same quota order number SID and geographical area id.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_origin_sid)

                # Business rule ON6	The validity period of the geographical area must span the validity period of the quota order number origin.
                geographical_area = g.app.get_geographical_area(geographical_area_sid)
                if len(geographical_area) > 0:
                    geo_validity_start_date = geographical_area[0]
                    geo_validity_end_date = geographical_area[1]
                    if validity_start_date < geo_validity_start_date or validity_end_date2 > geo_validity_end_date:
                        g.data_file.record_business_rule_violation("ON6", "The validity period of the geographical area must span the validity period of the quota order number origin.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_origin_sid)

                # Business rule ON7	The validity period of the quota order number must span the validity period of the quota order number origin.
                qon = g.app.get_quota_order_number(quota_order_number_sid)
                if len(qon) > 0:
                    qon_validity_start_date = qon[0]
                    qon_validity_end_date = qon[1]
                    if validity_start_date < qon_validity_start_date or validity_end_date2 > qon_validity_end_date:
                        g.data_file.record_business_rule_violation("ON7", "The validity period of the quota order number must span the validity period of the quota order number origin.", operation, transaction_id, message_id, record_code, sub_record_code, quota_order_number_origin_sid)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO quota_order_number_origins_oplog (quota_order_number_origin_sid,
            quota_order_number_sid, geographical_area_id, validity_start_date, validity_end_date,
            geographical_area_sid, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (quota_order_number_origin_sid,
            quota_order_number_sid, geographical_area_id, validity_start_date, validity_end_date,
            geographical_area_sid, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_order_number_sid) + " / " + geographical_area_id)
        cur.close()
