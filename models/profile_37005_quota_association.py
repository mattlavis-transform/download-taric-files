from datetime import datetime
import classes.globals as g


class QuotaAssociation(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        main_quota_definition_sid = g.app.get_number_value(message, ".//oub:main.quota.definition.sid", True)
        sub_quota_definition_sid = g.app.get_number_value(message, ".//oub:sub.quota.definition.sid", True)
        relation_type = g.app.get_value(message, ".//oub:relation.type", True)
        coefficient = g.app.get_value(message, ".//oub:coefficient", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota association", main_quota_definition_sid)

