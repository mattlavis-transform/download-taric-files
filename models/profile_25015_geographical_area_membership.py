from datetime import datetime
import classes.globals as g


class GeographicalAreaMembership(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        geographical_area_group_sid = g.app.get_number_value(message, ".//oub:geographical.area.group.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "geographical area membership", geographical_area_group_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            geographical_area_groups = g.app.get_geographical_area_groups()
            countries_regions = g.app.get_countries_regions()

            # Business rule GA12
            if geographical_area_sid not in countries_regions:
                g.data_file.record_business_rule_violation("GA12", "The referenced geographical area id (member) must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(geographical_area_sid))

            # Business rule GA14
            if geographical_area_group_sid is not None:
                if geographical_area_group_sid not in geographical_area_groups:
                    g.data_file.record_business_rule_violation("GA14", "The referenced geographical area group id must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(geographical_area_group_sid))

            # Business rule GA15 The membership start date must be less than or equal to the membership end date.
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("GA15", "The membership start date must be less than or equal to the membership end date.", operation, transaction_id, message_id, record_code, sub_record_code, str(geographical_area_sid))

            if update_type == "3":
                # Business rule GA16 The validity period of the geographical area group must span all membership periods of its members.
                sql = """select validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD')) as validity_end_date
                from geographical_areas where geographical_area_sid = %s order by validity_start_date desc limit 1;"""
                params = [
                    str(geographical_area_group_sid),
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) == 1:
                    geographical_area_group_start_date = rows[0][0]
                    geographical_area_group_end_date = rows[0][1]
                    if (validity_start_date < geographical_area_group_start_date) or (validity_end_date2 > geographical_area_group_end_date):
                        g.data_file.record_business_rule_violation("GA16", "The validity period of the geographical area group must span "
                        "all membership periods of its members.", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_sid)

                # Business rule GA18	When a geographical area is more than once member of the same group then there may be no overlap in their membership periods.
                similar_geographical_area_memberships_with_dates = g.app.get_similar_geographical_area_memberships_with_dates(geographical_area_group_sid, geographical_area_sid)
                if len(similar_geographical_area_memberships_with_dates) > 0:
                    for row in similar_geographical_area_memberships_with_dates:
                        existing_start_date = row[0]
                        existing_end_date = row[1]
                        # (StartDate1 <= EndDate2) and (StartDate2 <= EndDate1)
                        if (existing_start_date <= validity_end_date2) and (validity_start_date <= existing_end_date):
                            g.data_file.record_business_rule_violation("GA18", "When a geographical area is more than once member of the same "
                            "group then there may be no overlap in their membership periods.", operation, transaction_id, message_id,
                            record_code, sub_record_code, geographical_area_sid)
                            break



        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO geographical_area_memberships_oplog (geographical_area_sid,
            geographical_area_group_sid, validity_start_date, validity_end_date, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (geographical_area_sid,
            geographical_area_group_sid, validity_start_date, validity_end_date, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, geographical_area_sid)
        cur.close()
