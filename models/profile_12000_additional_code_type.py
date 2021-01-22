import classes.globals as g


class AdditionalCodeType(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        additional_code_type_id = g.app.get_value(message, ".//oub:additional.code.type.id", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        application_code = g.app.get_value(message, ".//oub:application.code", True)
        meursing_table_plan_id = g.app.get_value(message, ".//oub:meursing.table.plan.id", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "additional code type", additional_code_type_id)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            additional_code_types = g.app.get_additional_code_types()
            meursing_table_plans = g.app.get_meursing_table_plans()

            if update_type in ("1", "3"):  # UPDATE or INSERT
                # Business rule CT4
                if validity_end_date is not None:
                    if validity_end_date < validity_start_date:
                        g.data_file.record_business_rule_violation("CT4", "The start date must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

                if meursing_table_plan_id is not None:
                    # Business rule CT2
                    if application_code != 3:
                        g.data_file.record_business_rule_violation("CT2", "The Meursing table plan can only be entered if the additional code type has as application code 'Meursing table additional code type'.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

                    # Business rule CT3
                    if meursing_table_plan_id not in meursing_table_plans:
                        g.data_file.record_business_rule_violation("CT3", "The Meursing table plan must exist.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

            if update_type == "1":  # UPDATE
                # Business rule DBFK
                if additional_code_type_id not in additional_code_types:
                    g.data_file.record_business_rule_violation("DBFK", "The additional code type must exist.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

            elif update_type == "3":  # INSERT
                # Business rule CT1
                if additional_code_type_id in additional_code_types:
                    g.data_file.record_business_rule_violation("CT1", "The additional code type must be unique", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

            elif update_type == "2":  # DELETE
                used_non_meursing_additional_code_types = g.app.get_used_non_meursing_additional_code_types()
                additional_code_types_used_in_erns = g.app.get_additional_code_types_used_in_erns()
                additional_code_types_mapped_to_measure_types = g.app.get_additional_code_types_mapped_to_measure_types()

                # Business rule CT6
                if additional_code_type_id in used_non_meursing_additional_code_types:
                    g.data_file.record_business_rule_violation("CT6", "The additional code type cannot be deleted if it is related with a non-Meursing additional code.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

                # Business rule CT7
                if meursing_table_plan_id is not None:
                    if meursing_table_plan_id in meursing_table_plans:
                        g.data_file.record_business_rule_violation("CT7", "The additional code type cannot be deleted if it is related with a Meursing Table plan.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

                # Business rule CT9
                if additional_code_type_id in additional_code_types_used_in_erns:
                    g.data_file.record_business_rule_violation("CT9", "The additional code type cannot be deleted if it is related with an Export refund code.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

                # Business rule CT10
                if additional_code_type_id in additional_code_types_mapped_to_measure_types:
                    g.data_file.record_business_rule_violation("CT10", "The additional code type cannot be deleted if it is related with a measure type.", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO additional_code_types_oplog (additional_code_type_id, validity_start_date,
            validity_end_date, application_code, meursing_table_plan_id, operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (additional_code_type_id, validity_start_date,
            validity_end_date, application_code, meursing_table_plan_id, operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, additional_code_type_id)
        cur.close()
