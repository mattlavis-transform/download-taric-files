import classes.globals as g


class CompleteAbrogationRegulation(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        complete_abrogation_regulation_role = g.app.get_value(message, ".//oub:complete.abrogation.regulation.role", True)
        complete_abrogation_regulation_id = g.app.get_value(message, ".//oub:complete.abrogation.regulation.id", True)
        published_date = g.app.get_date_value(message, ".//oub:published.date", True)
        officialjournal_number = g.app.get_value(message, ".//oub:officialjournal.number", True)
        officialjournal_page = g.app.get_value(message, ".//oub:officialjournal.page", True)
        replacement_indicator = g.app.get_value(message, ".//oub:replacement.indicator", True)
        information_text = g.app.get_value(message, ".//oub:information.text", True)
        approved_flag = g.app.get_value(message, ".//oub:approved.flag", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "complete abrogation regulation", complete_abrogation_regulation_id)

