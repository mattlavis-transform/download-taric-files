import classes.globals as g


class QuotaClosedAndBalanceTransferredEvent(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_definition_sid = g.app.get_number_value(message, ".//oub:quota.definition.sid", True)
        occurrence_timestamp = g.app.get_value(message, ".//oub:occurrence.timestamp", True)
        closing_date = g.app.get_date_value(message, ".//oub:closing.date", True)
        transferred_amount = g.app.get_number_value(message, ".//oub:transferred.amount", True)
        target_quota_definition_sid = g.app.get_number_value(message, ".//oub:target.quota.definition.sid", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota closed and balance transferred event for quota definition", quota_definition_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if quota_definition_sid not in g.app.quota_definitions:
                g.data_file.record_business_rule_violation("QCTE1", "The quota definition SID must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO quota_unblocking_events_oplog (
            quota_definition_sid, occurrence_timestamp, closing_date, transferred_amount, target_quota_definition_sid, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (quota_definition_sid, occurrence_timestamp, closing_date, transferred_amount, target_quota_definition_sid, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, quota_definition_sid)
        cur.close()
