import classes.globals as g


class RegulationRoleTypeDescription(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        regulation_role_type_id = g.app.get_value(message, ".//oub:regulation.role.type.id", True)
        language_id = g.app.get_value(message, ".//oub:language.id", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "regulation role type description", regulation_role_type_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO regulation_role_type_descriptions_oplog (regulation_role_type_id, language_id, description, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (regulation_role_type_id, language_id, description, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, regulation_role_type_id)
        cur.close()
