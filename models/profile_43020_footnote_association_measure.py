import classes.globals as g


class FootnoteAssociationMeasure(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        code = footnote_type_id + footnote_id

        if measure_sid < 0:
            national = True
        else:
            national = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote association on measure_sid", measure_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):
                # Business rule FO5
                sql = """select 1 as idx, validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD'))
                from measures where measure_sid = %s union
                select 2 as idx, validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD'))
                from footnotes where footnote_type_id = %s and footnote_id = %s order by 1"""
                params = [
                    str(measure_sid),
                    footnote_type_id,
                    footnote_id
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) == 2:
                    measure_start_date = rows[0][1]
                    measure_end_date = rows[0][2]
                    footnote_start_date = rows[1][1]
                    footnote_end_date = rows[1][2]
                    if (footnote_start_date > measure_start_date) or (measure_end_date > footnote_end_date):
                        g.data_file.record_business_rule_violation("FO5", "When a footnote is used in a measure the validity period of the footnote "
                        "must span the validity period of the measure.", operation, transaction_id, message_id, record_code, sub_record_code, code)

                # Business rule DBFK
                sql = "select measure_sid from measures where measure_sid = %s limit 1"
                params = [
                    str(measure_sid)
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                try:
                    row = rows[0]
                    measure_exists = True
                except:
                    measure_exists = False

                if measure_exists is False:
                    g.data_file.record_business_rule_violation("DBFK", "Measure must exist (footnote association).", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnote_association_measures_oplog (measure_sid,
            footnote_type_id, footnote_id, operation, operation_date, national)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (measure_sid, footnote_type_id, footnote_id, operation, operation_date, national))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_sid)
        cur.close()
