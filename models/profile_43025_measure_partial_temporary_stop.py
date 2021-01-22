import classes.globals as g


class MeasurePartialTemporaryStop(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        partial_temporary_stop_regulation_id = g.app.get_value(message, ".//oub:partial.temporary.stop.regulation.id", True)
        partial_temporary_stop_regulation_officialjournal_number = g.app.get_value(message, ".//oub:partial.temporary.stop.regulation.officialjournal.number", True)
        partial_temporary_stop_regulation_officialjournal_page = g.app.get_value(message, ".//oub:partial.temporary.stop.regulation.officialjournal.page", True)
        abrogation_regulation_id = g.app.get_value(message, ".//oub:abrogation.regulation.id", True)
        abrogation_regulation_officialjournal_number = g.app.get_value(message, ".//oub:abrogation.regulation.officialjournal.number", True)
        abrogation_regulation_officialjournal_page = g.app.get_value(message, ".//oub:abrogation.regulation.officialjournal.page", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "partial temporary stop on measure_sid", measure_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            sql = "select measure_sid from measures where measure_sid = %s limit 1"
            params = [
                str(measure_sid)
            ]
            cur = g.app.conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            try:
                row = rows[0]
                measure_exists = True
            except:
                measure_exists = False

            if measure_exists is False:
                g.data_file.record_business_rule_violation("DBFK", "Measure must exist (partial temporary stop).", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measure_partial_temporary_stops_oplog (measure_sid, validity_start_date, validity_end_date,
            partial_temporary_stop_regulation_id, partial_temporary_stop_regulation_officialjournal_number,
            partial_temporary_stop_regulation_officialjournal_page, abrogation_regulation_id,
            abrogation_regulation_officialjournal_number, abrogation_regulation_officialjournal_page,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (measure_sid, validity_start_date, validity_end_date,
            partial_temporary_stop_regulation_id, partial_temporary_stop_regulation_officialjournal_number,
            partial_temporary_stop_regulation_officialjournal_page, abrogation_regulation_id,
            abrogation_regulation_officialjournal_number, abrogation_regulation_officialjournal_page,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_sid)
        cur.close()
