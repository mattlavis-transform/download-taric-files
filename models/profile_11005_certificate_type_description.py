import classes.globals as g


class CertificateTypeDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        certificate_type_code = g.app.get_value(message, ".//oub:certificate.type.code", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        certificate_type_descriptions = g.app.get_certificate_type_descriptions()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "certificate type description", certificate_type_code)

