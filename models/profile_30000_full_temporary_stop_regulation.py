import classes.globals as g


class FullTemporaryStopRegulation(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        full_temporary_stop_regulation_role = g.app.get_value(message, ".//oub:full.temporary.stop.regulation.role", True)
        full_temporary_stop_regulation_id = g.app.get_value(message, ".//oub:full.temporary.stop.regulation.id", True)
        published_date = g.app.get_date_value(message, ".//oub:published.date", True)
        officialjournal_number = g.app.get_value(message, ".//oub:officialjournal.number", True)
        officialjournal_page = g.app.get_value(message, ".//oub:officialjournal.page", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        effective_enddate = g.app.get_date_value(message, ".//oub:effective.enddate", True)
        complete_abrogation_regulation_role = g.app.get_value(message, ".//oub:complete.abrogation.regulation.role", True)
        complete_abrogation_regulation_id = g.app.get_value(message, ".//oub:complete.abrogation.regulation.id", True)
        explicit_abrogation_regulation_role = g.app.get_value(message, ".//oub:explicit.abrogation.regulation.role", True)
        explicit_abrogation_regulation_id = g.app.get_value(message, ".//oub:explicit.abrogation.regulation.id", True)
        replacement_indicator = g.app.get_value(message, ".//oub:replacement.indicator", True)
        information_text = g.app.get_value(message, ".//oub:information.text", True)
        approved_flag = g.app.get_value(message, ".//oub:approved.flag", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "full temporary stop regulation", full_temporary_stop_regulation_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO full_temporary_stop_regulations_oplog (full_temporary_stop_regulation_role,
            full_temporary_stop_regulation_id, published_date, officialjournal_number,
            officialjournal_page,
            validity_start_date, validity_end_date, effective_enddate,
            complete_abrogation_regulation_role, complete_abrogation_regulation_id,
            explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
            replacement_indicator, information_text, approved_flag,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (full_temporary_stop_regulation_role,
            full_temporary_stop_regulation_id, published_date, officialjournal_number,
            officialjournal_page,
            validity_start_date, validity_end_date, effective_enddate,
            complete_abrogation_regulation_role, complete_abrogation_regulation_id,
            explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
            replacement_indicator, information_text, approved_flag,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, full_temporary_stop_regulation_id)
        cur.close()
