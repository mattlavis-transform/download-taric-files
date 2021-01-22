import classes.globals as g


class MeasurementUnitQualifier(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measurement_unit_qualifier_code = g.app.get_value(message, ".//oub:measurement.unit.qualifier.code", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measurement unit qualifier", measurement_unit_qualifier_code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measurement_unit_qualifiers_oplog (measurement_unit_qualifier_code, validity_start_date,
            validity_end_date, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (measurement_unit_qualifier_code, validity_start_date, validity_end_date, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measurement_unit_qualifier_code)
        cur.close()
