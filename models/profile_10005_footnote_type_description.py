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

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            pass
            """
            if update_type in ("1", "3"):  # UPDATE / INSERT
                if footnote_type_id not in footnote_type_descriptions:
                    g.data_file.record_business_rule_violation("DBFK", "The footnote type must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)
            """

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnote_type_descriptions_oplog (footnote_type_id, language_id,
            description, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (footnote_type_id, language_id,
            description, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)
        cur.close()
