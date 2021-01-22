from datetime import datetime
import classes.globals as g


class BaseRegulation(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        base_regulation_role = g.app.get_value(message, ".//oub:base.regulation.role", True)
        base_regulation_id = g.app.get_value(message, ".//oub:base.regulation.id", True)
        code = base_regulation_role + base_regulation_id
        published_date = g.app.get_date_value(message, ".//oub:published.date", True)
        officialjournal_number = g.app.get_value(message, ".//oub:officialjournal.number", True)
        officialjournal_page = g.app.get_value(message, ".//oub:officialjournal.page", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        effective_end_date = g.app.get_date_value(message, ".//oub:effective.end.date", True)
        community_code = g.app.get_value(message, ".//oub:community.code", True)
        regulation_group_id = g.app.get_value(message, ".//oub:regulation.group.id", True)
        antidumping_regulation_role = g.app.get_value(message, ".//oub:antidumping.regulation.role", True)
        related_antidumping_regulation_id = g.app.get_value(message, ".//oub:related.antidumping.regulation.id", True)
        complete_abrogation_regulation_role = g.app.get_value(message, ".//oub:complete.abrogation.regulation.role", True)
        complete_abrogation_regulation_id = g.app.get_value(message, ".//oub:complete.abrogation.regulation.id", True)
        explicit_abrogation_regulation_role = g.app.get_value(message, ".//oub:explicit.abrogation.regulation.role", True)
        explicit_abrogation_regulation_id = g.app.get_value(message, ".//oub:explicit.abrogation.regulation.id", True)
        replacement_indicator = g.app.get_value(message, ".//oub:replacement.indicator", True)
        stopped_flag = g.app.get_value(message, ".//oub:stopped.flag", True)
        information_text = g.app.get_value(message, ".//oub:information.text", True)
        approved_flag = g.app.get_value(message, ".//oub:approved.flag", True)
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

        # Set operation types and print load message to screen
        national = None
        operation = g.app.get_loading_message(update_type, "base regulation", base_regulation_id)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            base_regulations = g.app.get_base_regulations()
            regulation_groups = g.app.get_regulation_groups()
            all_regulation_groups = g.app.get_all_regulation_groups()

            if update_type == "3":  # INSERT
                # Business rule ROIMB1
                if code in base_regulations:
                    g.data_file.record_business_rule_violation("ROIMB1", "The (regulation id + role id) must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)

            # Business rule ROIMB3
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("ROIMB3", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)

            # Business rule ROIMB4
            if regulation_group_id not in regulation_groups:
                g.data_file.record_business_rule_violation("ROIMB4", "The referenced regulation group must exist.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)

            # Business rule ROIMB47 The validity period of the regulation group id must span the validity period of the base regulation.
            for row in all_regulation_groups:
                rg_regulation_group_id = row[0]
                if rg_regulation_group_id == regulation_group_id:
                    rg_validity_start_date = row[1]
                    rg_validity_end_date = row[2]
                    if rg_validity_end_date < validity_end_date2 or rg_validity_start_date > validity_start_date:
                        g.data_file.record_business_rule_violation("ROIMB47", "The validity period of the regulation group id must span the validity period of the base regulation.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)
                    break

            if update_type == "1":  # UPDATE
                if validity_end_date is not None:
                    # Business rule ROIMB8 Explicit dates of related measures must be within the validity period of the base regulation.
                    sql = """select measure_sid, validity_start_date, validity_end_date from measures
                    where measure_generating_regulation_id = %s and measure_generating_regulation_role = %s
                    and validity_end_date is not null;"""
                    params = [
                        base_regulation_id,
                        base_regulation_role
                    ]
                    cur = g.app.conn.cursor()
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        for row in rows:
                            measure_sid = row[0]
                            measure_start_date = row[1]
                            measure_end_date = row[2]
                            if measure_end_date > validity_end_date:
                                g.data_file.record_business_rule_violation("ROIMB8", "Explicit dates of related measures must be within the validity period of the base regulation.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)

                    # Business rule ROIMB15	The validity period must span the start date of all related modification regulations.
                    related_modification_regulations = g.app.get_related_modification_regulations(base_regulation_id)
                    if len(related_modification_regulations) > 0:
                        for mr in related_modification_regulations:
                            if mr[2] > validity_end_date:
                                g.data_file.record_business_rule_violation("ROIMB15", "The validity period must span the start date of all related modification regulations.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO base_regulations_oplog (base_regulation_role,
            base_regulation_id, published_date, officialjournal_number, officialjournal_page,
            validity_start_date, validity_end_date, effective_end_date,
            community_code, regulation_group_id, antidumping_regulation_role,
            related_antidumping_regulation_id, complete_abrogation_regulation_role, complete_abrogation_regulation_id,
            explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
            replacement_indicator, stopped_flag, information_text, approved_flag,
            operation, operation_date, national)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (base_regulation_role,
            base_regulation_id, published_date, officialjournal_number, officialjournal_page,
            validity_start_date, validity_end_date, effective_end_date,
            community_code, regulation_group_id, antidumping_regulation_role,
            related_antidumping_regulation_id, complete_abrogation_regulation_role, complete_abrogation_regulation_id,
            explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
            replacement_indicator, stopped_flag, information_text, approved_flag,
            operation, operation_date, national))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)
        cur.close()

        if g.app.perform_taric_validation is True:
            g.app.all_regulations = g.app.get_all_regulations()
