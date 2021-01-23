import classes.globals as g


class PublicationSigle(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        code_type_id = g.app.get_value(message, ".//oub:code.type.id", True)
        code = g.app.get_value(message, ".//oub:code", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        publication_code = g.app.get_value(message, ".//oub:publication.code", True)
        publication_sigle = g.app.get_value(message, ".//oub:publication.sigle", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "publication sigle", code_type_id)

