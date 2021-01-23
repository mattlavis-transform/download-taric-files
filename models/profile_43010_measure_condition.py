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

