import classes.globals as g


class MeasureTypeSeries(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_type_series_id = g.app.get_value(message, ".//oub:measure.type.series.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        measure_type_combination = g.app.get_value(message, ".//oub:measure.type.combination", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measure type series", measure_type_series_id)

