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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("MT2", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, measure_type_id)

            if measure_type_series_id not in measure_type_series:
                g.data_file.record_business_rule_violation("MT2", "The referenced measure type series must exist.", operation, transaction_id, message_id, record_code, sub_record_code, measure_type_id)

            if update_type == "1":  # UPDATE
                if measure_type_id not in measure_types:
                    g.data_file.record_business_rule_violation("DBFK", "The referenced measure type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, measure_type_id)

            elif update_type == "3":  # INSERT
                if measure_type_id in measure_types:
                    g.data_file.record_business_rule_violation("MT1", "The measure type code must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, measure_type_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measure_types_oplog (measure_type_id, validity_start_date, validity_end_date,
            trade_movement_code, priority_code, measure_component_applicable_code,
            origin_dest_code, order_number_capture_code, measure_explosion_level,
            measure_type_series_id, operation, operation_date, national)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (measure_type_id, validity_start_date, validity_end_date,
            trade_movement_code, priority_code, measure_component_applicable_code,
            origin_dest_code, order_number_capture_code, measure_explosion_level,
            measure_type_series_id, operation, operation_date, national))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_type_id)
        cur.close()

        measure_types = g.app.get_measure_types()
