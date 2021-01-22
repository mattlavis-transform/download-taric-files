import classes.globals as g


class ProrogationRegulation(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        prorogation_regulation_role = g.app.get_value(message, ".//oub:prorogation.regulation.role", True)
        prorogation_regulation_id = g.app.get_value(message, ".//oub:prorogation.regulation.id", True)
        published_date = g.app.get_date_value(message, ".//oub:published.date", True)
        officialjournal_number = g.app.get_value(message, ".//oub:officialjournal.number", True)
        officialjournal_page = g.app.get_value(message, ".//oub:officialjournal.page", True)
        replacement_indicator = g.app.get_value(message, ".//oub:replacement.indicator", True)
        information_text = g.app.get_value(message, ".//oub:information.text", True)
        approved_flag = g.app.get_value(message, ".//oub:approved.flag", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "prorogation regulation", prorogation_regulation_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO prorogation_regulations_oplog (prorogation_regulation_role,
            prorogation_regulation_id, published_date, officialjournal_number,
            officialjournal_page, replacement_indicator, information_text, approved_flag,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (prorogation_regulation_role,
            prorogation_regulation_id, published_date, officialjournal_number,
            officialjournal_page, replacement_indicator, information_text, approved_flag,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, prorogation_regulation_id)
        cur.close()

        if g.app.perform_taric_validation is True:
            g.app.all_regulations = g.app.get_all_regulations()
