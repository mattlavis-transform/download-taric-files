import classes.globals as g


class QuotaDefinition(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_definition_sid = g.app.get_number_value(message, ".//oub:quota.definition.sid", True)
        quota_order_number_id = g.app.get_value(message, ".//oub:quota.order.number.id", True)
        quota_order_number_sid = g.app.get_number_value(message, ".//oub:quota.order.number.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        volume = g.app.get_value(message, ".//oub:volume", True)
        initial_volume = g.app.get_value(message, ".//oub:initial.volume", True)
        monetary_unit_code = g.app.get_value(message, ".//oub:monetary.unit.code", True)
        measurement_unit_code = g.app.get_value(message, ".//oub:measurement.unit.code", True)
        measurement_unit_qualifier_code = g.app.get_value(message, ".//oub:measurement.unit.qualifier.code", True)
        maximum_precision = g.app.get_value(message, ".//oub:maximum.precision", True)
        critical_state = g.app.get_value(message, ".//oub:critical.state", True)
        critical_threshold = g.app.get_value(message, ".//oub:critical.threshold", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota definition", quota_definition_sid)

