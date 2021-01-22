import classes.globals as g


class FootnoteAssociationMeursingHeading(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        meursing_table_plan_id = g.app.get_number_value(message, ".//oub:meursing.table.plan.id", True)
        meursing_heading_number = g.app.get_value(message, ".//oub:meursing.heading.number", True)
        row_column_code = g.app.get_value(message, ".//oub:row.column.code", True)
        footnote_type = g.app.get_value(message, ".//oub:footnote.type", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote association for Meursing heading text for Meursing heading number", meursing_heading_number)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO footnote_association_meursing_headings_oplog (meursing_table_plan_id, meursing_heading_number,
            row_column_code, footnote_type, footnote_id, validity_start_date, validity_end_date, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (meursing_table_plan_id, meursing_heading_number,
            row_column_code, footnote_type, footnote_id, validity_start_date, validity_end_date, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, meursing_heading_number)
        cur.close()
