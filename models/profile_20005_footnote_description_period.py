import classes.globals as g


class FootnoteDescriptionPeriod(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        footnote_description_period_sid = g.app.get_number_value(message, ".//oub:footnote.description.period.sid", True)
        footnote_type_id = g.app.get_value(message, ".//oub:footnote.type.id", True)
        footnote_id = g.app.get_value(message, ".//oub:footnote.id", True)
        code = footnote_type_id + footnote_id
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)

        if footnote_description_period_sid < 0:
            national = True
        else:
            national = None

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "footnote description period", footnote_type_id + str(footnote_id) + " (" + str(validity_start_date) + ")")

