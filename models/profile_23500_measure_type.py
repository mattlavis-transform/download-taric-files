import classes.globals as g


class MeasureType(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_type_id = g.app.get_value(message, ".//oub:measure.type.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        trade_movement_code = g.app.get_value(message, ".//oub:trade.movement.code", True)
        priority_code = g.app.get_value(message, ".//oub:priority.code", True)
        measure_component_applicable_code = g.app.get_value(message, ".//oub:measure.component.applicable.code", True)
        origin_dest_code = g.app.get_value(message, ".//oub:origin.dest.code", True)
        order_number_capture_code = g.app.get_value(message, ".//oub:order.number.capture.code", True)
        measure_explosion_level = g.app.get_value(message, ".//oub:measure.explosion.level", True)
        measure_type_series_id = g.app.get_value(message, ".//oub:measure.type.series.id", True)

        measure_types = g.app.get_measure_types()
        measure_type_series = g.app.get_measure_type_series()
        if not(measure_type_id.isnumeric()):
            national = True
        else:
            national = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measure type", measure_type_id)

