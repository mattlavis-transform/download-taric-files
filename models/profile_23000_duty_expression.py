import classes.globals as g


class DutyExpression(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        duty_expression_id = g.app.get_value(message, ".//oub:duty.expression.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        duty_amount_applicability_code = g.app.get_number_value(message, ".//oub:duty.amount.applicability.code", True)
        measurement_unit_applicability_code = g.app.get_number_value(message, ".//oub:measurement.unit.applicability.code", True)
        monetary_unit_applicability_code = g.app.get_number_value(message, ".//oub:monetary.unit.applicability.code", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "duty expression", duty_expression_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO duty_expressions_oplog (duty_expression_id, validity_start_date,
            validity_end_date, duty_amount_applicability_code, measurement_unit_applicability_code, monetary_unit_applicability_code,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (duty_expression_id, validity_start_date, validity_end_date,
            duty_amount_applicability_code, measurement_unit_applicability_code, monetary_unit_applicability_code,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, duty_expression_id)
        cur.close()
