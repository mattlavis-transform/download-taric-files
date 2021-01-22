import classes.globals as g


class CertificateDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        certificate_description_period_sid = g.app.get_number_value(message, ".//oub:certificate.description.period.sid", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        certificate_type_code = g.app.get_value(message, ".//oub:certificate.type.code", True)
        certificate_code = g.app.get_value(message, ".//oub:certificate.code", True)
        code = certificate_type_code + certificate_code
        description = g.app.get_value(message, ".//oub:description", True)

        certificate_types = g.app.get_certificate_types()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "certificate description", certificate_type_code + certificate_code)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type == "1":  # UPDATE
                if certificate_type_code not in certificate_types:
                    g.data_file.record_business_rule_violation("CE1", "The referenced certificate type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, code)

            elif update_type == "3":  # INSERT
                if certificate_type_code not in certificate_types:
                    g.data_file.record_business_rule_violation("CE1", "The referenced certificate type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO certificate_descriptions_oplog (certificate_description_period_sid, language_id,
            certificate_type_code, certificate_code, description, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (certificate_description_period_sid, language_id,
            certificate_type_code, certificate_code, description, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, code)
        cur.close()
