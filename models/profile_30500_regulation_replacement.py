import classes.globals as g


class RegulationReplacement(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        replacing_regulation_role = g.app.get_value(message, ".//oub:replacing.regulation.role", True)
        replacing_regulation_id = g.app.get_value(message, ".//oub:replacing.regulation.id", True)
        replaced_regulation_role = g.app.get_value(message, ".//oub:replaced.regulation.role", True)
        replaced_regulation_id = g.app.get_value(message, ".//oub:replaced.regulation.id", True)
        measure_type_id = g.app.get_value(message, ".//oub:measure.type.id", True)
        geographical_area_id = g.app.get_value(message, ".//oub:geographical.area.id", True)
        chapter_heading = g.app.get_value(message, ".//oub:chapter.heading", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "regulation replacement", replacing_regulation_id)

