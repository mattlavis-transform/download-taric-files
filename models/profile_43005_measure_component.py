import classes.globals as g


class MeasureComponent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        duty_expression_id = g.app.get_value(message, ".//oub:duty.expression.id", True)
        duty_amount = g.app.get_value(message, ".//oub:duty.amount", True)
        monetary_unit_code = g.app.get_value(message, ".//oub:monetary.unit.code", True)
        measurement_unit_code = g.app.get_value(message, ".//oub:measurement.unit.code", True)
        measurement_unit_qualifier_code = g.app.get_value(message, ".//oub:measurement.unit.qualifier.code", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measure component on measure_sid", measure_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            # Business rule ME50 The combination measurement unit + measurement unit qualifier must exist.
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
                    g.data_file.record_business_rule_violation("ME50", "The combination measurement unit + measurement unit qualifier must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME41 error
            if duty_expression_id not in g.app.duty_expressions:
                g.data_file.record_business_rule_violation("ME41", "The referenced duty expression must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME45, ME46 and ME47 errors
            if duty_expression_id in g.app.duty_expressions:
                for item in g.app.all_duty_expressions:
                    duty_expression_id2 = item[0]
                    validity_start_date = item[1]
                    validity_end_date = item[2]
                    duty_amount_applicability_code = item[3]
                    measurement_unit_applicability_code = item[4]
                    monetary_unit_applicability_code = item[5]

                    if duty_expression_id == duty_expression_id2:
                        # ME45
                        if duty_amount_applicability_code == 1:  # Mandatory
                            if duty_amount is None:
                                g.data_file.record_business_rule_violation("ME45(a)", "If the flag 'amount' on duty expression is 'mandatory' then an amount must "
                                "be specified. If the flag is set 'not permitted' then no amount may be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                        elif duty_amount_applicability_code == 2:  # Not permitted
                            if duty_amount is not None:
                                g.data_file.record_business_rule_violation("ME45(b)", "If the flag 'amount' on duty expression is 'mandatory' then an amount must "
                                "be specified. If the flag is set 'not permitted' then no amount may be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

                        # ME46
                        if monetary_unit_applicability_code == 1:  # Mandatory
                            if monetary_unit_code is None:
                                g.data_file.record_business_rule_violation("ME46(a)", "If the flag 'monetary unit' on duty expression is 'mandatory' then a monetary unit "
                                "must be specified. If the flag is set 'not permitted' then no monetary unit may be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                        elif monetary_unit_applicability_code == 2:  # Not permitted
                            if monetary_unit_code is not None:
                                g.data_file.record_business_rule_violation("ME46(b)", "If the flag 'monetary unit' on duty expression is 'mandatory' then a monetary unit "
                                "must be specified. If the flag is set 'not permitted' then no monetary unit may be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

                        # ME47
                        if measurement_unit_applicability_code == 1:  # Mandatory
                            if measurement_unit_code is None:
                                g.data_file.record_business_rule_violation("ME47(a)", "If the flag 'measurement unit' on duty expression is 'mandatory' then a "
                                "measurement unit must be specified. If the flag is set 'not permitted' then no measurement unit may be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                        elif measurement_unit_applicability_code == 2:  # Not permitted
                            if measurement_unit_code is None:
                                g.data_file.record_business_rule_violation("ME47(b)", "If the flag 'measurement unit' on duty expression is 'mandatory' then a "
                                "measurement unit must be specified. If the flag is set 'not permitted' then no measurement unit may be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                        break

        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):
                sql = "select measure_sid from measures where measure_sid = " + str(measure_sid) + " limit 1"
                cur = g.app.conn.cursor()
                cur.execute(sql)
                rows = cur.fetchall()
                try:
                    row = rows[0]
                    measure_exists = True
                except:
                    measure_exists = False

                if measure_exists is False:
                    g.data_file.record_business_rule_violation("DBFK", "Measure must exist (measure component).", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measure_components_oplog (measure_sid, duty_expression_id, duty_amount,
            monetary_unit_code, measurement_unit_code,
            measurement_unit_qualifier_code, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (measure_sid, duty_expression_id, duty_amount,
            monetary_unit_code, measurement_unit_code,
            measurement_unit_qualifier_code, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_sid)
        cur.close()
