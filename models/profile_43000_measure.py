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

        # Add to a global list of measures, so that this can be validated at the end that there are
        # components associated with it
        if g.app.perform_taric_validation is True:
            if measure_type in g.app.measure_types_that_require_components_list:
                g.app.duty_measure_list.append(measure_sid)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "measure", measure_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            if update_type in ("1", "3"):  # UPDATE OR INSERT
                # Business rule NIG30 When a goods nomenclature is used in a goods measure then the validity
                # period of the goods nomenclature  must span the validity period of the goods measure.
                sql = """select goods_nomenclature_item_id, producline_suffix, validity_start_date,
                coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD')) from goods_nomenclatures
                where goods_nomenclature_sid = %s order by validity_start_date desc;"""
                params = [
                    goods_nomenclature_sid,
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                match = True
                for row in rows:
                    goods_nomenclature_start_date = row[2]
                    goods_nomenclature_end_date = row[3]
                    if (validity_start_date < goods_nomenclature_start_date) or (validity_end_date2 > goods_nomenclature_end_date):
                        match = False
                    else:
                        match = True
                        break

                if match is False:
                    g.data_file.record_business_rule_violation("NIG30", "When a goods nomenclature is used in a goods measure then the validity "
                    "period of the goods nomenclature must span the validity period of the goods measure.", operation,
                    transaction_id, message_id, record_code, sub_record_code, measure_sid)
                    sys.exit()

                # Business rule GA10
                # When a geographical area is referenced in a measure then the validity period of
                # the geographical area must span the validity period of the measure.
                sql = """select validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD')) as validity_end_date
                from geographical_areas where geographical_area_id = %s order by validity_start_date desc limit 1;"""
                params = [
                    str(geographical_area),
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) == 1:
                    geographical_area_start_date = rows[0][0]
                    geographical_area_end_date = rows[0][1]
                    if (validity_start_date < geographical_area_start_date) or (validity_end_date2 > geographical_area_end_date):
                        g.data_file.record_business_rule_violation("GA10", "When a geographical area is referenced in a measure then the validity period of "
                        "the geographical area must span the validity period of the measure", operation, transaction_id, message_id, record_code, sub_record_code, measure_sid)

                # Business rule ACN13
                # When an additional code is used in an additional code nomenclature measure then the validity
                # period of the additional code must span the validity period of the measure.
                if additional_code_sid is not None:
                    if validity_end_date is None:
                        validity_end_date2 = datetime.strptime("2999-12-31", "%Y-%m-%d")
                    else:
                        validity_end_date2 = validity_end_date
                    sql = """select validity_start_date, coalesce(validity_end_date, TO_DATE('2999-12-31', 'YYYY-MM-DD')) as validity_end_date
                    from additional_codes where additional_code_sid = %s;"""
                    params = [
                        str(additional_code_sid),
                    ]
                    cur = g.app.conn.cursor()
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                    if len(rows) == 1:
                        additional_code_start_date = rows[0][0]
                        additional_code_end_date = rows[0][1]
                        if (additional_code_start_date > validity_start_date) or (validity_end_date2 > additional_code_end_date):
                            g.data_file.record_business_rule_violation("ACN13", "When an additional code is used in an additional code nomenclature measure "
                            "then the validity period of the additional code must span the validity period of the measure.", operation,
                            transaction_id, message_id, record_code, sub_record_code, measure_sid)

            # Not a Taric error, but just simple referential integrity
            # Check if a delete is being made, and if so, check that the measure exists before actually deleting
            if int(update_type) == 2:  # Delete
                sql = "select measure_sid from measures where measure_sid = %s"
                params = [
                    str(measure_sid)
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) == 0:
                    g.data_file.record_business_rule_violation("DBFK", "The measure must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME34 error
            if validity_end_date is not None:
                if justification_regulation_id is None or justification_regulation_role is None:
                    g.data_file.record_business_rule_violation("ME34", "A justification regulation must be entered if the measure end date is filled in.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME86 error
            if int(measure_generating_regulation_role) > 4:
                g.data_file.record_business_rule_violation("ME86", "The role of the entered regulation must be a Base, a Modification, "
                "a Provisional AntiDumping, a Definitive Anti-Dumping.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME6 / ME7 error
            """
            if (goods_nomenclature_item_id not in g.app.goods_nomenclatures) and (goods_nomenclature_item_id is not None):
                g.data_file.record_business_rule_violation("ME6", "The goods code must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
            """

            # Check for ME4 error
            geographical_areas = g.app.get_all_geographical_areas()
            if geographical_area not in geographical_areas:
                g.data_file.record_business_rule_violation("ME4", "The geographical area must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME2, ME3 and ME10 error
            measure_types = g.app.get_measure_types()
            if measure_type not in measure_types:
                g.data_file.record_business_rule_violation("ME2", "The measure type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
            else:
                ME3_Error = False
                for item in g.app.all_measure_types:
                    measure_type_id2 = item[0]
                    validity_start_date2 = item[1]
                    validity_end_date2 = item[2]
                    order_number_capture_code = item[3]

                    if measure_type_id2 == measure_type:
                        # first check for ME10 (order_number_capture_code)
                        if (order_number_capture_code == 2 and ordernumber is not None) or (order_number_capture_code == 1 and ordernumber is None):
                            g.data_file.record_business_rule_violation("ME10", "The order number must be specified if the 'order number flag' "
                            "(specified in the measure type record) has the value 'mandatory'. If the flag is set "
                            "to 'not permitted' then the field cannot be entered.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                        if validity_end_date is None:
                            if validity_end_date2 is None:
                                if validity_start_date < validity_start_date2:
                                    ME3_Error = True
                            else:
                                if validity_start_date > validity_end_date2:
                                    ME3_Error = True
                        else:
                            if validity_end_date2 is None:
                                if validity_start_date < validity_start_date2:
                                    ME3_Error = True
                            else:
                                if validity_start_date < validity_start_date2 or validity_end_date > validity_end_date2:
                                    ME3_Error = True
                        break
                if ME3_Error is True:
                    g.data_file.record_business_rule_violation("ME3", "The validity period of the measure type must span the validity period of the measure.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Check for ME25 error
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("ME3", "If the measure’s end date is specified (implicitly or explicitly) then "
                    "the start date of the measure must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            if int(update_type) in (3, 1):
                if ordernumber is not None:
                    found = False
                    for item in g.app.all_quota_order_numbers:
                        quota_order_number_id2 = item[0]
                        quota_order_number_sid2 = item[1]
                        validity_start_date2 = item[2]
                        validity_end_date2 = item[3]
                        if str(measure_sid) == "3682137":
                            a = 1
                        if ordernumber == quota_order_number_id2:
                            found = True
                            break

                    if found is False:
                        if ordernumber[0:3] != "094":
                            g.data_file.record_business_rule_violation("ME116", "When a quota order number is used in a measure then the "
                            "validity period of the quota order number must span the validity period of the measure.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                    else:
                        # Business rule ON9
                        ON9_error = False
                        if validity_end_date2 is None:
                            if validity_start_date < validity_start_date2:
                                ON9_error = True
                        else:
                            if validity_end_date > validity_end_date2 or validity_start_date < validity_start_date2:
                                ON9_error = True

                        if ON9_error is True:
                            pass
                            """
                            if validity_start_date > datetime.strptime("2007-12-31", "%Y-%m-%d"):
                                g.data_file.record_business_rule_violation("ON9", "When a quota order number is used in a measure, then the validity period " \
                                "of the quota order number must span the validity period of the measure.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                            """

            # run ME24 check - check that there is a supporting regulation
            if regulation_code not in g.app.all_regulations:
                g.data_file.record_business_rule_violation("ME24", "The role + regulation id must exist. If no measure start date is specified, it defaults to the regulation start date.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            # Run ROIMB8 check - that dates of measures fall within dates of regulation
            my_regulation = g.app.get_my_regulation(regulation_code)
            if my_regulation is not None:
                regulation_start_date = my_regulation[2]
                regulation_end_date = my_regulation[3]

                if validity_end_date is None:
                    # Step 1 - check for when the measure end date is not specified
                    # print("Measure start date", validity_start_date, "Regulation start date", regulation_start_date)
                    if validity_start_date < regulation_start_date:
                        g.data_file.record_business_rule_violation("ROIMB8(a)", "Explicit dates of related measures must be within the "
                        "validity period of the base regulation.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                else:
                    # Step 2 - check for when the measure end date is specified
                    if regulation_end_date is None:
                        if validity_start_date < regulation_start_date:
                            print(validity_start_date, regulation_start_date, measure_sid)
                            g.data_file.record_business_rule_violation("ROIMB8(b)", "Explicit dates of related measures must be within the "
                            "validity period of the base regulation.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

                    else:
                        pass
                        """
                        if validity_start_date < regulation_start_date or validity_end_date > regulation_end_date:
                            g.data_file.record_business_rule_violation("ROIMB8(c)", "Explicit dates of related measures must be within the "
                            "validity period of the base regulation.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                        """

            # Not a business rule, but a major flaw in Taric - this prevents a SID being inserted
            # if it already exists
            if int(update_type) == 3:
                sql = "select measure_sid from measures_oplog where measure_sid = %s"
                params = [
                    str(measure_sid)
                ]
                cur = g.app.conn.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                if len(rows) > 0:
                    g.data_file.record_business_rule_violation("DBFK", "Measure SID already exists", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))

            check_me32 = True
            if check_me32 is True:
                # run ME32 check - get relations of this commodity code up and down the tree
                if int(update_type) == 3:
                    if goods_nomenclature_sid is not None:
                        my_node = g.app.find_node(goods_nomenclature_item_id)
                        relation_string = "'" + goods_nomenclature_item_id + "', "
                        for relation in my_node.relations:
                            relation_string += "'" + relation + "', "
                        relation_string = relation_string.strip(", ")

                        sql = "select measure_sid from utils.measures_real_end_dates m \n" \
                            "where \n" \
                            "(\n" \
                            "	measure_type_id = '" + measure_type + "' \n"  \
                            "	and goods_nomenclature_item_id in (" + relation_string + ") \n"

                        if geographical_area is None:
                            sql += "	and geographical_area_id is Null \n"
                        else:
                            sql += "	and geographical_area_id = '" + geographical_area + "' \n"

                        if ordernumber is None:
                            sql += "	and ordernumber is Null \n"
                        else:
                            sql += "	and ordernumber = '" + ordernumber + "' \n"

                        if reduction_indicator is None:
                            sql += "	and reduction_indicator is Null \n"
                        else:
                            sql += "	and reduction_indicator = '" + str(reduction_indicator) + "' \n"

                        if additional_code_type is None:
                            sql += "	and additional_code_type_id is Null \n"
                        else:
                            sql += "	and additional_code_type_id = '" + additional_code_type + "' \n"

                        if additional_code is None:
                            sql += "	and additional_code_id is Null \n"
                        else:
                            sql += "	and additional_code_id = '" + additional_code + "' \n"

                        sql += ")\nand\n(\n"

                        if validity_end_date is None:
                            # The new measure does not have an end date
                            sql += """  (validity_end_date is null or (validity_start_date <= '""" + validity_start_date_string + """'
                            and validity_end_date >= '""" + validity_start_date_string + """')))"""
                        else:
                            # The new measure has an end date
                            sql += """
            (
                validity_end_date is not Null and
                (
                    ('""" + validity_start_date_string + """' <= validity_start_date and '""" + validity_end_date_string + """' >= validity_start_date)
                    or
                    ('""" + validity_start_date_string + """' <= validity_end_date and '""" + validity_end_date_string + """' >= validity_end_date)
                )
            )
            or
            (
                validity_end_date is Null and
                (
                    '""" + validity_start_date_string + """' >= validity_start_date or '""" + validity_end_date_string + """' >= validity_start_date
                )
            )
        """

                            sql += ")\n"

                        cur = g.app.conn.cursor()
                        cur.execute(sql)
                        rows = cur.fetchall()
                        if len(rows) > 0:
                            rw = rows[0]
                            offended_measure_sid = rw[0]
                            g.data_file.record_business_rule_violation("ME32", "There may be no overlap in time with other measure occurrences with a goods code "
                            "in the same nomenclature hierarchy which references the same measure type, geo area, order number, additional code and reduction "
                            "indicator. This rule is not applicable for Meursing additional codes.", operation, transaction_id, message_id, record_code, sub_record_code, str(measure_sid))
                            sys.exit()

        tariff_measure_number = goods_nomenclature_item_id
        if goods_nomenclature_item_id is not None:
            if tariff_measure_number[-2:] == "00":
                tariff_measure_number = tariff_measure_number[:-2]

        if measure_sid < 0:
            national = True
        else:
            national = None

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO measures_oplog (measure_sid, measure_type_id, geographical_area_id,
            goods_nomenclature_item_id, additional_code_type_id, additional_code_id,
            ordernumber, reduction_indicator, validity_start_date,
            measure_generating_regulation_role, measure_generating_regulation_id, validity_end_date,
            justification_regulation_role, justification_regulation_id, stopped_flag,
            geographical_area_sid, goods_nomenclature_sid, additional_code_sid,
            export_refund_nomenclature_sid, operation, operation_date, national, tariff_measure_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (measure_sid, measure_type, geographical_area,
            goods_nomenclature_item_id, additional_code_type, additional_code,
            ordernumber, reduction_indicator, validity_start_date,
            measure_generating_regulation_role, measure_generating_regulation_id, validity_end_date,
            justification_regulation_role, justification_regulation_id, stopped_flag,
            geographical_area_sid, goods_nomenclature_sid, additional_code_sid,
            export_refund_nomenclature_sid, operation, operation_date, national, tariff_measure_number))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, measure_sid)
        cur.close()
