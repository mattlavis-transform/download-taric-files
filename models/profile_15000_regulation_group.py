import sys
import classes.globals as g


class RegulationGroup(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        regulation_group_id = g.app.get_value(message, ".//oub:regulation.group.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        regulation_groups = g.app.get_regulation_groups()

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "regulation group", regulation_group_id)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):  # UPDATE or INSERT
                # Business rule RG3
                if validity_end_date is not None:
                    if validity_end_date < validity_start_date:
                        g.data_file.record_business_rule_violation("RG3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, regulation_group_id)

            if update_type == "1":  # UPDATE
                # Business rule DBFK
                if regulation_group_id not in regulation_groups:
                    g.data_file.record_business_rule_violation("DBFK", "The regulation group must exist.", operation, transaction_id, message_id, record_code, sub_record_code, regulation_group_id)

            elif update_type == "2":  # DELETE
                used_regulation_groups = g.app.get_used_regulation_groups()
                # Business rule DBFK
                if regulation_group_id not in regulation_groups:
                    g.data_file.record_business_rule_violation("DBFK", "The regulation group must exist.", operation, transaction_id, message_id, record_code, sub_record_code, regulation_group_id)

                # Business rule RG2
                if regulation_group_id not in used_regulation_groups:
                    g.data_file.record_business_rule_violation("RG2", "The Regulation group cannot be deleted if it is used in a base regulation.", operation, transaction_id, message_id, record_code, sub_record_code, regulation_group_id)

            elif update_type == "3":  # INSERT
                # Business rule RG1
                if regulation_group_id in regulation_groups:
                    g.data_file.record_business_rule_violation("RG1", "The Regulation group id must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, regulation_group_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO regulation_groups_oplog (regulation_group_id, validity_start_date,
            validity_end_date, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (regulation_group_id, validity_start_date, validity_end_date, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, regulation_group_id)
        cur.close()
