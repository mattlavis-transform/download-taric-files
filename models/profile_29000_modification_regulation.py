import classes.globals as g
import sys
from datetime import datetime


class ModificationRegulation(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        modification_regulation_role = g.app.get_value(message, ".//oub:modification.regulation.role", True)
        modification_regulation_id = g.app.get_value(message, ".//oub:modification.regulation.id", True)
        published_date = g.app.get_date_value(message, ".//oub:published.date", True)
        officialjournal_number = g.app.get_value(message, ".//oub:officialjournal.number", True)
        officialjournal_page = g.app.get_value(message, ".//oub:officialjournal.page", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        effective_end_date = g.app.get_date_value(message, ".//oub:effective.end.date", True)
        base_regulation_role = g.app.get_value(message, ".//oub:base.regulation.role", True)
        base_regulation_id = g.app.get_value(message, ".//oub:base.regulation.id", True)
        complete_abrogation_regulation_role = g.app.get_value(message, ".//oub:complete.abrogation.regulation.role", True)
        complete_abrogation_regulation_id = g.app.get_value(message, ".//oub:complete.abrogation.regulation.id", True)
        explicit_abrogation_regulation_role = g.app.get_value(message, ".//oub:explicit.abrogation.regulation.role", True)
        explicit_abrogation_regulation_id = g.app.get_value(message, ".//oub:explicit.abrogation.regulation.id", True)
        replacement_indicator = g.app.get_value(message, ".//oub:replacement.indicator", True)
        stopped_flag = g.app.get_value(message, ".//oub:stopped.flag", True)
        information_text = g.app.get_value(message, ".//oub:information.text", True)
        approved_flag = g.app.get_value(message, ".//oub:approved.flag", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "modification regulation", modification_regulation_id)

        # Perform business rule validation
        # Get the earlier of the 2 - effective or validity end dates
        if g.app.perform_taric_validation is True:
            if update_type == "3":
                # Business rule ROIMM1	The (regulation id + role id) must be unique.
                for reg in g.app.all_regulations_with_dates:
                    if modification_regulation_id == reg[0] and modification_regulation_role == reg[1]:
                        g.data_file.record_business_rule_violation("ROIMM1", "The (regulation id + role id) must be unique.", operation,
                        transaction_id, message_id, record_code, sub_record_code, modification_regulation_id)
                        break

            if update_type in ("1", "3"):
                if validity_end_date is not None:
                    # Business rule ROIMM14	Explicit dates of related measures must be within the validity period of the modification regulation.
                    sql = """select measure_sid, validity_start_date, validity_end_date from measures
                    where measure_generating_regulation_id = %s and measure_generating_regulation_role = %s
                    and validity_end_date is not null;"""
                    params = [
                        modification_regulation_id,
                        modification_regulation_role
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
                                g.data_file.record_business_rule_violation("ROIMM14", "Explicit dates of related measures must be within the "
                                "validity period of the modification regulation.", operation, transaction_id, message_id, record_code, sub_record_code, base_regulation_id)

                # ROIMM5	The start date must be less than or equal to the end date if the end date is explicit.
                if validity_end_date is not None:
                    if validity_end_date < validity_start_date:
                        g.data_file.record_business_rule_violation("ROIMM5", "The start date must be less than or equal to the end date if the end date is explicit.", operation, transaction_id, message_id, record_code, sub_record_code, modification_regulation_id)

            if validity_end_date is not None and effective_end_date is not None:
                if validity_end_date < effective_end_date:
                    my_end_date = validity_end_date
                else:
                    my_end_date = effective_end_date
            elif validity_end_date is not None:
                my_end_date = validity_end_date
            elif effective_end_date is not None:
                my_end_date = effective_end_date
            else:
                my_end_date = None

            """
            if my_end_date is not None:
                my_end_date_string = my_end_date.strftime("%Y-%m-%d")

                if validity_end_date is not None or effective_end_date is not None:
                    sql = "select measure_sid from utils.measures_real_end_dates " \
                    "where measure_generating_regulation_id = %s and measure_generating_regulation_role = %s' " \
                    "and validity_end_date is not null and validity_end_date > %s order by measure_sid"

                    params = [
                        modification_regulation_id,
                        modification_regulation_role,
                        my_end_date_string
                    ]

                    cur = g.app.conn.cursor()
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        offending_measures = ""
                        for row in rows:
                            offending_measures += str(row[0]) + ", "

                        g.data_file.record_business_rule_violation("MODx", "Clashing modification regulation", operation, transaction_id, message_id, record_code, sub_record_code, modification_regulation_id + "(" + offending_measures + ")")
            """

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO modification_regulations_oplog (modification_regulation_role,
            modification_regulation_id, published_date, officialjournal_number, officialjournal_page,
            validity_start_date, validity_end_date, effective_end_date,
            base_regulation_role, base_regulation_id,
            complete_abrogation_regulation_role, complete_abrogation_regulation_id,
            explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
            replacement_indicator, stopped_flag, information_text, approved_flag,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (modification_regulation_role,
            modification_regulation_id, published_date, officialjournal_number, officialjournal_page,
            validity_start_date, validity_end_date, effective_end_date,
            base_regulation_role, base_regulation_id,
            complete_abrogation_regulation_role, complete_abrogation_regulation_id,
            explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
            replacement_indicator, stopped_flag, information_text, approved_flag,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, modification_regulation_id)
        cur.close()

        if g.app.perform_taric_validation is True:
            g.app.all_regulations = g.app.get_all_regulations()
