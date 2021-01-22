import classes.globals as g


class ProrogationRegulationAction(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        prorogation_regulation_role = g.app.get_value(message, ".//oub:prorogation.regulation.role", True)
        prorogation_regulation_id = g.app.get_value(message, ".//oub:prorogation.regulation.id", True)
        prorogated_regulation_role = g.app.get_value(message, ".//oub:prorogated.regulation.role", True)
        prorogated_regulation_id = g.app.get_value(message, ".//oub:prorogated.regulation.id", True)
        prorogated_date = g.app.get_date_value(message, ".//oub:prorogated.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "prorogation regulation action", prorogation_regulation_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO prorogation_regulation_actions_oplog (prorogation_regulation_role,
            prorogation_regulation_id, prorogated_regulation_role, prorogated_regulation_id, prorogated_date,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (prorogation_regulation_role,
            prorogation_regulation_id, prorogated_regulation_role, prorogated_regulation_id, prorogated_date,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, prorogation_regulation_id)
        cur.close()
