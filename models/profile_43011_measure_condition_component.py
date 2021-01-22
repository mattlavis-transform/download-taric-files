import classes.globals as g


class MeasureConditionComponent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_condition_sid = g.app.get_number_value(message, ".//oub:measure.condition.sid", True)
        duty_expression_id = g.app.get_value(message, ".//oub:duty.expression.id", True)
        duty_amount = g.app.get_value(message, ".//oub:duty.amount", True)
        monetary_unit_code = g.app.get_value(message, ".//oub:monetary.unit.code", True)
        measurement_unit_code = g.app.get_value(message, ".//oub:measurement.unit.code", True)
        measurement_unit_qualifier_code = g.app.get_value(message, ".//oub:measurement.unit.qualifier.code", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "Measure condition component", measure_condition_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            # Business rule ME62 The combination measurement unit + measurement unit qualifier must exist.
            if measurement_unit_qualifier_code is not None:
                measurements = g.app.get_measurements()
                measurement_matched = False
                for item in measurements:
                    item_measurement_unit_code = item[0]
                    item_measurement_unit_qualifier_code = item[1]
                    if item_measurement_unit_code == measurement_unit_code and item_measurement_unit_qualifier_code == measurement_unit_qualifier_code:
                        measurement_matched = True
                        break
                if measurement_matched is False:
                    g.data_file.record_business_rule_violation("ME62", "The combination measurement unit + measurement unit qualifier must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_condition_sid))

            if update_type in ("1", "3"):  # UPDATE or insert
                # Business rule DBFK
                sql = "select measure_condition_sid from measure_conditions where measure_condition_sid = %s"
                params = [
                    str(measure_condition_sid)
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) == 0:
                    g.data_file.record_business_rule_violation("ME53", "The referenced measure condition must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_condition_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measure_condition_components_oplog (measure_condition_sid, duty_expression_id, duty_amount,
            monetary_unit_code, measurement_unit_code,
            measurement_unit_qualifier_code, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (measure_condition_sid, duty_expression_id, duty_amount,
            monetary_unit_code, measurement_unit_code,
            measurement_unit_qualifier_code, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_condition_sid)
        cur.close()
