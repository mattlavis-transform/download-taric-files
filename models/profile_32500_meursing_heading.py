import classes.globals as g


class MeursingHeading(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        meursing_table_plan_id = g.app.get_number_value(message, ".//oub:meursing.table.plan.id", True)
        meursing_heading_number = g.app.get_value(message, ".//oub:meursing.heading.number", True)
        row_column_code = g.app.get_value(message, ".//oub:row.column.code", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "Meursing heading", meursing_heading_number)

