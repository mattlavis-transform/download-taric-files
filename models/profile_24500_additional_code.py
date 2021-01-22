import classes.globals as g


class AdditionalCode(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_sid = g.app.get_number_value(message, ".//oub:additional.code.sid", True)
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code//oub:additional.code", True)
        code = additional_code_type_id + additional_code
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "additional code", code)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            # Business rule CE 3
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("ACN3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, code)

            if update_type in ("1", "3"):  # UPDATE AND INSERT
                additional_code_types = g.app.get_additional_code_types()

                # Business rule ACN2
                if additional_code_type_id not in additional_code_types:
                    g.data_file.record_business_rule_violation("ACN2", "The referenced additional code type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, code)

            elif update_type == "2":  # DELETE
                # Business rule ACN14	An additional code cannot be deleted if it is used in an additional code nomenclature measure.
                used_additional_codes = g.app.get_used_additional_codes()
                if additional_code_sid in used_additional_codes:
                    g.data_file.record_business_rule_violation("ACN14", "An additional code cannot be deleted if it is used in an additional code nomenclature measure.", operation, transaction_id, message_id, record_code, sub_record_code, code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO additional_codes_oplog (additional_code_sid, additional_code_type_id, additional_code,
            validity_start_date, validity_end_date, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (additional_code_sid, additional_code_type_id, additional_code,
            validity_start_date, validity_end_date, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, code)
        cur.close()
