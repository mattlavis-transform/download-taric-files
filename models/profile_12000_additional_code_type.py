import classes.globals as g


class AdditionalCodeType(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        application_code = g.app.get_value(message, ".//oub:application.code", True)
        meursing_table_plan_id = g.app.get_value(message, ".//oub:meursing.table.plan.id", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "additional code type", additional_code_type_id)

