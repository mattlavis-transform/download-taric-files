import classes.globals as g


class AdditionalCodeTypeDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        additional_code_type_descriptions = g.app.get_additional_code_type_descriptions()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "additional code type description", additional_code_type_id)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type == "1":  # UPDATE
                if additional_code_type_id not in additional_code_type_descriptions:
                    g.data_file.record_business_rule_violation("DBFK", "The additional code type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO additional_code_type_descriptions_oplog (additional_code_type_id, language_id,
            description, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (additional_code_type_id, language_id,
            description, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)
        cur.close()
