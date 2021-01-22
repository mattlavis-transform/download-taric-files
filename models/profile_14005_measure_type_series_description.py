import classes.globals as g


class MeasureTypeSeriesDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_type_series_id = g.app.get_value(message, ".//oub:measure.type.series.id", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measure type series description", measure_type_series_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measure_type_series_descriptions_oplog (measure_type_series_id, language_id,
            description, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (measure_type_series_id, language_id,
            description, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_type_series_id)
        cur.close()
