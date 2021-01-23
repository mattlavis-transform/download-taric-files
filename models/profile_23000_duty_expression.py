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

