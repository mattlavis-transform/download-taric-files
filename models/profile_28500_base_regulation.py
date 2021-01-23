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

