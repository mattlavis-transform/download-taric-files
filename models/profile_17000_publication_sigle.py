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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):  # UPDATE or INSERT
                # Business rule PS3
                if validity_end_date is not None:
                    if validity_end_date < validity_start_date:
                        g.data_file.record_business_rule_violation("PS3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, publication_code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO publication_sigles_oplog (code_type_id, code, validity_start_date,
            validity_end_date, publication_code, publication_sigle, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (code_type_id, code, validity_start_date, validity_end_date, publication_code, publication_sigle, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, publication_sigle)
        cur.close()
