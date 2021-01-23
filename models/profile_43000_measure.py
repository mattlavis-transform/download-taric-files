import sys
import classes.globals as g
from classes.classification import classification
from datetime import datetime


class Measure(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        measure_sid = g.app.get_number_value(message, ".//oub:measure.sid", True)
        measure_type = g.app.get_value(message, ".//oub:measure.type", True)
        geographical_area = g.app.get_value(message, ".//oub:geographical.area", True)
        goods_nomenclature_item_id = g.app.get_value(message, ".//oub:goods.nomenclature.item.id", True)
        additional_code_type = g.app.get_value(message, ".//oub:additional.code.type", True)
        additional_code = g.app.get_value(message, ".//oub:additional.code", True)
        ordernumber = g.app.get_value(message, ".//oub:ordernumber", True)
        reduction_indicator = g.app.get_number_value(message, ".//oub:reduction.indicator", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_start_date_string = g.app.get_value(message, ".//oub:validity.start.date", True)
        measure_generating_regulation_role = g.app.get_value(message, ".//oub:measure.generating.regulation.role", True)
        measure_generating_regulation_id = g.app.get_value(message, ".//oub:measure.generating.regulation.id", True)
        regulation_code = measure_generating_regulation_id
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        validity_end_date_string = g.app.get_value(message, ".//oub:validity.end.date", True)
        justification_regulation_role = g.app.get_value(message, ".//oub:justification.regulation.role", True)
        justification_regulation_id = g.app.get_value(message, ".//oub:justification.regulation.id", True)
        stopped_flag = g.app.get_value(message, ".//oub:stopped.flag", True)
        geographical_area_sid = g.app.get_number_value(message, ".//oub:geographical.area.sid", True)
        goods_nomenclature_sid = g.app.get_number_value(message, ".//oub:goods.nomenclature.sid", True)
        additional_code_sid = g.app.get_number_value(message, ".//oub:additional.code.sid", True)
        export_refund_nomenclature_sid = g.app.get_number_value(message, ".//oub:export.refund.nomenclature.sid", True)
        if validity_end_date is None:
            validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            validity_end_date2 = validity_end_date

