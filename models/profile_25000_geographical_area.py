from datetime import datetime
import classes.globals as g


class GeographicalArea(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        geographical_area_id = g.app.get_value(message, ".//oub:geographical.area.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        geographical_code = g.app.get_value(message, ".//oub:geographical.code", True)
        parent_geographical_area_group_sid = g.app.get_number_value(message, ".//oub:parent.geographical.area.group.sid", True)
        validity_start_date_string = validity_start_date.strftime('%Y-%m-%d')
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

        geographical_area_groups = g.app.get_geographical_area_groups()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "geographical area", geographical_area_id)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            # Business rule GA2
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("GA2", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_id)

            # Business rule GA4
            if parent_geographical_area_group_sid is not None:
                if parent_geographical_area_group_sid not in geographical_area_groups:
                    g.data_file.record_business_rule_violation("GA4", " The referenced parent geographical area group must be an existing geographical "
                    "area with area code = 1 (geographical area group).", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_id)

            if update_type == "3":
                # Business rule GA1 The combination geographical area id + validity start date must be unique.
                geographical_areas_with_dates = g.app.get_geographical_areas_with_dates()
                if geographical_area_id + "_" + validity_start_date_string in geographical_areas_with_dates:
                    g.data_file.record_business_rule_violation("GA1", "The combination geographical area id + validity start date must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_id)

                # Business rule GA7	The validity period of geographical area must not overlap any other geographical area with the same geographical area id.
                similar_geographical_areas_with_dates = g.app.get_similar_geographical_areas_with_dates(geographical_area_id)
                print(len(similar_geographical_areas_with_dates))
                for row in similar_geographical_areas_with_dates:
                    existing_start_date = row[1]
                    existing_end_date = row[2]
                    # (StartDate1 <= EndDate2) and (StartDate2 <= EndDate1)
                    if (existing_start_date <= validity_end_date2) and (validity_start_date <= existing_end_date):
                        g.data_file.record_business_rule_violation("GA7", "The validity period of geographical area must not overlap any other geographical area with the same geographical area id.", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_id)
                        break


        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO geographical_areas_oplog (geographical_area_sid, geographical_area_id,
            validity_start_date, validity_end_date, geographical_code,
            parent_geographical_area_group_sid, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (geographical_area_sid, geographical_area_id,
            validity_start_date, validity_end_date, geographical_code,
            parent_geographical_area_group_sid, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_id)
        cur.close()

        if g.app.perform_taric_validation is True:
            g.app.geographical_area_sids = g.app.get_all_geographical_area_sids()
            g.app.geographical_areas = g.app.get_all_geographical_areas()
