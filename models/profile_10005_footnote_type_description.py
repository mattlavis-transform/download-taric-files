import classes.globals as g


class FootnoteTypeDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        footnote_type_descriptions = g.app.get_footnote_type_descriptions()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote type description", footnote_type_id + " (" + description + ")")

