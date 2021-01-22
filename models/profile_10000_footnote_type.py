import classes.globals as g


class FootnoteType(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        application_code = g.app.get_value(message, ".//oub:application.code", True)

        footnote_types = g.app.get_footnote_types()

        # Check if national
        if footnote_type_id in ('01', '02', '03', '05', '05', '06'):
            national = True
        else:
            national = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote type", footnote_type_id)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):	  # UPDATE or INSERT
                # BUSINESS RULE FOT3
                if validity_end_date is not None:
                    if validity_end_date < validity_start_date:
                        g.data_file.record_business_rule_violation("FOT3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)

            if update_type == "1":  # UPDATE
                # BUSINESS RULE DBFK
                if footnote_type_id not in footnote_types:
                    g.data_file.record_business_rule_violation("DBFK", "The footnote type must exist for footnote type updates.", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)

            if update_type == "3":  # INSERT
                # BUSINESS RULE FOT01
                if footnote_type_id in footnote_types:
                    g.data_file.record_business_rule_violation("FOT1", "The footnote type must be unique", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)

            if update_type == "2":  # DELETE
                # BUSINESS RULE FOT02
                sql = "select count(*) from footnotes where footnote_type_id = %s;"
                params = [
                    footnote_type_id
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) != 0:
                    g.data_file.record_business_rule_violation("FOT2", "The footnote type cannot be deleted if it is used in a footnote.", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnote_types_oplog (footnote_type_id, validity_start_date,
            validity_end_date, application_code, operation, operation_date, national)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (footnote_type_id, validity_start_date, validity_end_date, application_code, operation, operation_date, national))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, footnote_type_id)
        cur.close()
