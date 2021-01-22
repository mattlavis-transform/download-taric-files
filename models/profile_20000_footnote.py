import classes.globals as g


class Footnote(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        code = footnote_type_id + footnote_id
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        if footnote_type_id in ('01', '02', '03', '05', '05', '06'):
            national = True
        else:
            national = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote", footnote_type_id + str(footnote_id))

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            footnote_types = g.app.get_footnote_types()
            footnotes = g.app.get_footnotes()

            if update_type in ("1", "3"):  # INSERT
                # Business rule FO3
                if validity_end_date is not None:
                    if validity_end_date < validity_start_date:
                        g.data_file.record_business_rule_violation("FO3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, code)

                # Business rule FO1
                if footnote_type_id not in footnote_types:
                    g.data_file.record_business_rule_violation("FO1", "The referenced footnote type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, code)

            if update_type == "3":  # INSERT
                # Business rule FO1
                if code in footnotes:
                    g.data_file.record_business_rule_violation("FO2", "The combination footnote type and code must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, code)

            elif update_type == "2":  # DELETE
                # Business rule FO11	When a footnote is used in a measure then the footnote may not be deleted.
                used_footnote_codes = g.app.get_used_footnote_codes()
                if code in used_footnote_codes:
                    g.data_file.record_business_rule_violation("FO11", "When a footnote is used in a measure then the footnote may not be deleted.", operation, transaction_id, message_id, record_code, sub_record_code, code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnotes_oplog (footnote_type_id, footnote_id, validity_start_date,
            validity_end_date, operation, operation_date, national)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (footnote_type_id, footnote_id, validity_start_date, validity_end_date, operation, operation_date, national))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, code)
        cur.close()
