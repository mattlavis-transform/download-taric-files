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

