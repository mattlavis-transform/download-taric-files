import classes.globals as g


class QuotaDefinition(object):
    def parse_node(self, app, update_type, message, transaction_id, message_id, record_code, sub_record_code):
        g.app.message_count += 1
        operation_date = g.app.get_timestamp()
        quota_definition_sid = g.app.get_number_value(message, ".//oub:quota.definition.sid", True)
        quota_order_number_id = g.app.get_value(message, ".//oub:quota.order.number.id", True)
        quota_order_number_sid = g.app.get_number_value(message, ".//oub:quota.order.number.sid", True)
        validity_start_date = g.app.get_date_value(message, ".//oub:validity.start.date", True)
        validity_end_date = g.app.get_date_value(message, ".//oub:validity.end.date", True)
        volume = g.app.get_value(message, ".//oub:volume", True)
        initial_volume = g.app.get_value(message, ".//oub:initial.volume", True)
        monetary_unit_code = g.app.get_value(message, ".//oub:monetary.unit.code", True)
        measurement_unit_code = g.app.get_value(message, ".//oub:measurement.unit.code", True)
        measurement_unit_qualifier_code = g.app.get_value(message, ".//oub:measurement.unit.qualifier.code", True)
        maximum_precision = g.app.get_value(message, ".//oub:maximum.precision", True)
        critical_state = g.app.get_value(message, ".//oub:critical.state", True)
        critical_threshold = g.app.get_value(message, ".//oub:critical.threshold", True)
        description = g.app.get_value(message, ".//oub:description", True)

        # Set operation types and print load message to screen
        operation = g.app.get_loading_message(update_type, "quota definition", quota_definition_sid)

        # Perform business rule validation
        if g.app.perform_taric_validation is True:
            # Business rule QD2	The start date must be less than or equal to the end date
            if validity_end_date is None:
                g.data_file.record_business_rule_violation("QDx", "The quota definition must have an end date.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

            # Business rule QD2	The start date must be less than or equal to the end date
            if validity_end_date is not None:
                if validity_end_date < validity_start_date:
                    g.data_file.record_business_rule_violation("QD2", "The start date of the quota definition must be less than or equal to the end date.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

            # Business rule QD3	The quota order number must exist
            found = False
            for item in g.app.all_quota_order_numbers:
                quota_order_number_id2 = item[0]
                quota_order_number_sid2 = item[1]
                validity_start_date2 = item[2]
                validity_end_date2 = item[3]
                if quota_order_number_sid == quota_order_number_sid2:
                    found = True
                    break

            if found is False:
                g.data_file.record_business_rule_violation("QD3", "The quota order number must exist.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

            if update_type in ("1", "3"):
                found = False
                for item in g.app.all_quota_definitions:
                    quota_definition_sid2 = item[0]
                    quota_order_number_id2 = item[1]
                    validity_start_date2 = item[2]
                    validity_end_date2 = item[3]
                    if quota_order_number_id2 == quota_order_number_id:
                        if validity_start_date2 == validity_start_date:
                            if quota_definition_sid2 != quota_definition_sid:
                                found = True
                                break
                            else:
                                if update_type == "3":
                                    g.data_file.record_business_rule_violation("DBFK", "Quota definition is a duplicate.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

                # Business rule QD1	Quota order number id + start date must be unique.
                if found is True:
                    g.data_file.record_business_rule_violation("QD1", "Quota order number id + start date must be unique.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

            if update_type == "3":  # INSERT
                if found is True:
                    # Business rule ON8
                    if validity_end_date2 is not None:
                        if (validity_end_date > validity_end_date2) or (validity_start_date < validity_start_date2):
                            g.data_file.record_business_rule_violation("ON8(a)", "The validity period of the quota order number must span the validity "
                            "period of the referencing quota definition.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))
                    else:
                        if validity_start_date < validity_start_date2:
                            g.data_file.record_business_rule_violation("ON8(b)", "The validity period of the quota order number must span the validity "
                            "period of the referencing quota definition.", operation, transaction_id, message_id, record_code, sub_record_code, str(quota_definition_sid))

        # Load data
        cur = g.app.conn.cursor()
        try:
            cur.execute("""INSERT INTO quota_definitions_oplog (quota_definition_sid, quota_order_number_id, validity_start_date,
            validity_end_date, volume, initial_volume, quota_order_number_sid,
            monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code,
            maximum_precision, critical_state, critical_threshold, description,
            operation, operation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (quota_definition_sid, quota_order_number_id, validity_start_date,
            validity_end_date, volume, initial_volume, quota_order_number_sid,
            monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code,
            maximum_precision, critical_state, critical_threshold, description,
            operation, operation_date))
            g.app.conn.commit()
        except:
            g.data_file.record_business_rule_violation("DB", "DB failure", operation, transaction_id, message_id, record_code, sub_record_code, quota_definition_sid)
        cur.close()

        if g.app.perform_taric_validation is True:
            g.app.quota_definitions = g.app.get_quota_definitions()
