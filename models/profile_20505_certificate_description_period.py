import classes.globals as g


class CertificateDescriptionPeriod(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        certificate_description_period_sid = g.app.get_number_value(message, ".//oub:certificate.description.period.sid", True)
        certificate_type_code = g.app.get_value(message, ".//oub:certificate.type.code", True)
        certificate_code = g.app.get_value(message, ".//oub:certificate.code", True)
        code = certificate_type_code + certificate_code
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "certificate", certificate_description_period_sid)

