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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type == "1":	  # UPDATE
                if certificate_type_code not in certificate_type_descriptions:
                    g.data_file.record_business_rule_violation("DBFK", "The footnote type must exist", operation, transaction_id, message_id, record_code, sub_record_code, certificate_type_code)

            elif update_type == "3":	  # INSERT
                if certificate_type_code in certificate_type_descriptions:
                    g.data_file.record_business_rule_violation("CET1", "The type of the certificate must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, certificate_type_code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO certificate_type_descriptions_oplog (certificate_type_code, language_id,
            description, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (certificate_type_code, language_id,
            description, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, certificate_type_code)
        cur.close()
