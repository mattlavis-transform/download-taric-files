import classes.globals as g


class MeursingTableCellComponent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        meursing_additional_code_sid = g.app.get_number_value(message, ".//oub:meursing.additional.code.sid", True)
        meursing_table_plan_id = g.app.get_number_value(message, ".//oub:meursing.table.plan.id", True)
        heading_number = g.app.get_value(message, ".//oub:heading.number", True)
        row_column_code = g.app.get_value(message, ".//oub:row.column.code", True)
        subheading_sequence_number = g.app.get_number_value(message, ".//oub:subheading.sequence.number", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "Meursing table cell component", additional_code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO meursing_table_cell_components_oplog (meursing_additional_code_sid,
            meursing_table_plan_id, heading_number, row_column_code, subheading_sequence_number,
            validity_start_date, validity_end_date, additional_code, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (meursing_additional_code_sid,
            meursing_table_plan_id, heading_number, row_column_code, subheading_sequence_number,
            validity_start_date, validity_end_date, additional_code, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, additional_code)
        cur.close()
