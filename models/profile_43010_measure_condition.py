import classes.globals as g


class MeasureCondition(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_condition_sid = g.app.get_number_value(message, ".//oub:measure.condition.sid", True)
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        condition_code = g.app.get_value(message, ".//oub:condition.code", True)
        component_sequence_number = g.app.get_value(message, ".//oub:component.sequence.number", True)
        condition_duty_amount = g.app.get_value(message, ".//oub:condition.duty.amount", True)
        condition_monetary_unit_code = g.app.get_value(message, ".//oub:condition.monetary.unit.code", True)
        condition_measurement_unit_code = g.app.get_value(message, ".//oub:condition.measurement.unit.code", True)
        condition_measurement_unit_qualifier_code = g.app.get_value(message, ".//oub:condition.measurement.unit.qualifier.code", True)
        action_code = g.app.get_value(message, ".//oub:action.code", True)
        certificate_type_code = g.app.get_value(message, ".//oub:certificate.type.code", True)
        certificate_code = g.app.get_value(message, ".//oub:certificate.code", True)
        if certificate_type_code is not None:
            code = certificate_type_code + certificate_code
        else:
            code = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measure condition on measure_sid", measure_sid)

        # Perform business rule validation
        # A measure must exist for a measure condition to be inserted or updated (not deleted, as this may have happened in the same transaction)
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):
                sql = "select count(measure_sid) from measures where measure_sid = %s"
                params = [
                    str(measure_sid)
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                row = cur.fetchone()
                if row[0] == 0:
                    g.data_file.record_business_rule_violation("DBFK", "Measure must exist (measure condition).", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # You must not be able to insert a new measure condition if that measure condition already exists
            if update_type == "3":
                sql = "select count(measure_sid) from measure_conditions where measure_condition_sid = %s"
                params = [
                    str(measure_condition_sid)
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                row = cur.fetchone()
                if row[0] == 1:
                    g.data_file.record_business_rule_violation("DBFK", "Measure condition already exists: cannot overwrite.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

                # Business rule CE4	If a certificate is used in a measure condition then the validity period of the certificate must span the validity period of the measure.
                if code is not None:
                    sql = """select validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD')) as validity_end_date, 1 as idx
                    from measures where measure_sid = %s union
                    select validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD')) as validity_end_date, 2 as idx
                    from certificates where certificate_type_code = %s and certificate_code = %s
                    order by 3;"""
                    params = [
                        str(measure_sid),
                        certificate_type_code,
                        certificate_code
                    ]
                    cur = g.app.conn.cursor()
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    if len(rows) == 2:
                        measure_start_date = rows[0][0]
                        measure_end_date = rows[0][1]
                        certificate_start_date = rows[1][0]
                        certificate_end_date = rows[1][1]
                        if (certificate_start_date > measure_start_date) or (measure_end_date > certificate_end_date):
                            g.data_file.record_business_rule_violation("CE4", "If a certificate is used in a measure condition then the validity period of the "
                            "certificate must span the validity period of the measure.", operation, transaction_id, message_id, record_code, sub_record_code, code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measure_conditions_oplog (measure_condition_sid, measure_sid, condition_code,
            component_sequence_number, condition_duty_amount, condition_monetary_unit_code,
            condition_measurement_unit_code, condition_measurement_unit_qualifier_code, action_code,
            certificate_type_code, certificate_code, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (measure_condition_sid, measure_sid, condition_code,
            component_sequence_number, condition_duty_amount, condition_monetary_unit_code,
            condition_measurement_unit_code, condition_measurement_unit_qualifier_code, action_code,
            certificate_type_code, certificate_code, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_sid)
        cur.close()
