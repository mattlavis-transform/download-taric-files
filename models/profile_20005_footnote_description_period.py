import classes.globals as g


class FootnoteDescriptionPeriod(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        footnote_description_period_sid = g.app.get_number_value(message, ".//oub:footnote.description.period.sid", True)
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        code = footnote_type_id + footnote_id
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)

        footnote_types = g.app.get_footnote_types()
        if footnote_description_period_sid < 0:
            national = True
        else:
            national = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote description period", footnote_type_id + str(footnote_id) + " (" + str(validity_start_date) + ")")

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if footnote_type_id not in footnote_types:
                g.data_file.record_business_rule_violation("FO1", "The referenced footnote type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, code)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnote_description_periods_oplog (footnote_description_period_sid,
            footnote_type_id, footnote_id, validity_start_date, operation, operation_date, national)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (footnote_description_period_sid, footnote_type_id, footnote_id, validity_start_date, operation, operation_date, national))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, code)
        cur.close()
