from datetime import datetime
import os
import json
import csv
import xlsxwriter
from classes.database import Database
from classes.quota_definition import QuotaDefinition
from classes.quota_balance import QuotaBalance
from classes.measure import Measure
from classes.measure_component import MeasureComponent
from classes.excel import Excel

import classes.globals as g


class QuotaHandler(object):
    def __init__(self):
        self.quota_definitions = []
        self.quota_balances = []
        self.measures = []
        self.measure_components = []

    def get_quotas(self):
        print("Getting quotas")
        sql = """
        select quota_definition_sid, quota_order_number_id,
        validity_start_date, validity_end_date,
        initial_volume, measurement_unit_code, measurement_unit_qualifier_code,
        critical_state, critical_threshold
        from quota_definitions qd
        where validity_start_date <= current_date
        and validity_end_date >= current_date
        order by quota_order_number_id         
        """
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            quota_definition = QuotaDefinition()
            quota_definition.quota_definition_sid = row[0]
            quota_definition.quota_order_number_id = row[1]
            quota_definition.validity_start_date = row[2]
            quota_definition.validity_end_date = row[3]
            quota_definition.initial_volume = row[4]
            quota_definition.volume = quota_definition.initial_volume
            quota_definition.measurement_unit_code = row[5]
            quota_definition.measurement_unit_qualifier_code = row[6]
            quota_definition.critical_state = row[7]
            quota_definition.critical_threshold = row[8]

            self.quota_definitions.append(quota_definition)

    def get_quota_balances(self):
        print("Getting balances")
        sql = """
        with cte as (
            select distinct on (qd.quota_definition_sid)
            qd.quota_definition_sid, quota_order_number_id, qbe.occurrence_timestamp, qbe.new_balance
            from quota_definitions qd, quota_balance_events qbe 
            where qd.quota_definition_sid = qbe.quota_definition_sid
            and validity_start_date <= current_date
            and validity_end_date >= current_date
            order by quota_definition_sid, occurrence_timestamp desc
        ) select * from cte order by quota_order_number_id         
        """
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            quota_balance = QuotaBalance()
            quota_balance.quota_definition_sid = row[0]
            quota_balance.quota_order_number_id = row[1]
            quota_balance.occurrence_timestamp = row[2]
            quota_balance.new_balance = row[3]

            self.quota_balances.append(quota_balance)

    def get_quota_measure_components(self):
        print("Getting measure components")
        sql = """
        select m.measure_sid, mc.duty_expression_id, mc.duty_amount,
        mc.monetary_unit_code, mc.measurement_unit_code, mc.measurement_unit_qualifier_code
        from utils.materialized_measures_real_end_dates m, measure_components mc 
        where validity_start_date::date <= current_date 
        and (validity_end_date::date >= current_date or validity_end_date is null)
        and m.measure_type_id in ('122', '123', '143', '146', '122', '122', '653', '654')
        and m.measure_sid = mc.measure_sid
        order by m.measure_sid, mc.duty_expression_id
        """
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            mc = MeasureComponent()
            mc.measure_sid = row[0]
            mc.duty_expression_id = row[1]
            mc.duty_amount = row[2]
            mc.monetary_unit_code = row[3]
            mc.measurement_unit_code = row[4]
            mc.measurement_unit_qualifier_code = row[5]

            self.measure_components.append(mc)
        pass
    
    def get_measures(self):
        print("Getting measures")
        self.get_quota_measure_components()
        sql = """
        select measure_sid, goods_nomenclature_item_id, ordernumber, geographical_area_id,
        m.measure_type_id, mtd.description as measure_type_description,
        m.validity_start_date, m.validity_end_date 
        from utils.materialized_measures_real_end_dates m, measure_type_descriptions mtd 
        where validity_start_date::date <= current_date 
        and (validity_end_date::date >= current_date or validity_end_date is null)
        and m.measure_type_id in ('122', '123', '143', '146', '122', '122', '653', '654')
        and m.measure_type_id = mtd.measure_type_id
        order by ordernumber, goods_nomenclature_item_id, measure_type_id
        """
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            measure = Measure()
            measure.measure_sid = row[0]
            measure.goods_nomenclature_item_id = row[1]
            measure.quota_order_number_id = row[2]
            measure.geographical_area_id = row[3]
            measure.measure_type_id = row[4]
            measure.measure_type_description = row[5]
            measure.validity_start_date = row[6]
            measure.validity_end_date = row[7]

            self.measures.append(measure)
            
        self.assign_measure_components()
        self.build_duties()
        
    def assign_measure_components(self):
        print("Assigning measure components")
        for mc in self.measure_components:
            for m in self.measures:
                if mc.measure_sid == m.measure_sid:
                    m.measure_components.append(mc)
                    
    def build_duties(self):
        for m in self.measures:
            m.build_duty()

    def assign_quota_balances(self):
        print("Assigning quota balances")
        for quota_definition in self.quota_definitions:
            for quota_balance in self.quota_balances:
                if quota_balance.quota_definition_sid == quota_definition.quota_definition_sid:
                    quota_definition.volume = quota_balance.new_balance
                    break

    def write_excel(self):
        print("Writing Excel")
        self.excel = Excel()
        today = datetime.now()
        
        filename = "eu_quotas_" + datetime.strftime(today, "%Y-%m-%d") + ".xlsx"
        self.excel.create_excel(g.app.quotas_folder, filename)
        self.write_balances()
        self.write_measures()
        self.close_excel()
        print("Done")
        
    def write_measures(self):
        self.get_units()
        worksheet = self.excel.workbook.add_worksheet("Measures")
        data = ('SID', 'Quota order number', 'Commodity', 'Origin', 'Measure type', 'Start date', 'End date', 'In quota duty')
        worksheet.write_row('A1', data, self.excel.format_bold)
        worksheet.set_column(0, 6, 20)
        worksheet.set_column(4, 4, 40)
        worksheet.set_column(7, 7, 60)
        worksheet.freeze_panes(1, 0)

        row_count = 1
        for measure in self.measures:
            for unit in self.units:
                measure.duty = measure.duty.replace(unit["unit"], unit["friendly"])
            
            worksheet.write(row_count, 0, measure.measure_sid, self.excel.format_wrap)
            worksheet.write(row_count, 1, measure.quota_order_number_id, self.excel.format_wrap)
            worksheet.write(row_count, 2, measure.goods_nomenclature_item_id, self.excel.format_wrap)
            worksheet.write(row_count, 3, measure.geographical_area_id, self.excel.format_number)
            worksheet.write(row_count, 4, measure.measure_type_description, self.excel.format_wrap)
            worksheet.write(row_count, 5, measure.validity_start_date, self.excel.format_wrap)
            worksheet.write(row_count, 6, measure.validity_end_date, self.excel.format_wrap)
            worksheet.write(row_count, 7, measure.duty, self.excel.format_wrap)

            row_count += 1
            
        worksheet.autofilter('A1:H' + str(row_count))
        
    def get_units(self):
        data_folder = os.getcwd()
        data_folder = os.path.join(data_folder, "data")
        unit_file = os.path.join(data_folder, "units.json")
        with open(unit_file) as json_file:
            self.units = json.load(json_file)
            
    
    def write_balances(self):
        worksheet = self.excel.workbook.add_worksheet("Quota balances")
        data = ('SID', 'Quota order number', 'Period start date', 'Period end date', 'Initial volume', 'Current volume', 'Measurement', 'Critical state', 'Critical threshold')
        worksheet.write_row('A1', data, self.excel.format_bold)
        worksheet.set_column(0, 9, 20)
        worksheet.freeze_panes(1, 0)

        row_count = 1
        for quota_definition in self.quota_definitions:
            unit = quota_definition.measurement_unit_code if quota_definition.measurement_unit_qualifier_code is None else quota_definition.measurement_unit_code + ' ' + quota_definition.measurement_unit_qualifier_code

            worksheet.write(row_count, 0, quota_definition.quota_definition_sid, self.excel.format_wrap)
            worksheet.write(row_count, 1, quota_definition.quota_order_number_id, self.excel.format_wrap)
            worksheet.write(row_count, 2, datetime.strftime(quota_definition.validity_start_date, "%Y-%m-%d"), self.excel.format_wrap)
            worksheet.write(row_count, 3, quota_definition.validity_end_date, self.excel.format_wrap)
            worksheet.write(row_count, 4, quota_definition.initial_volume, self.excel.format_number)
            worksheet.write(row_count, 5, quota_definition.volume, self.excel.format_number)
            worksheet.write(row_count, 6, unit, self.excel.format_wrap)
            worksheet.write(row_count, 7, quota_definition.critical_state, self.excel.format_wrap)
            worksheet.write(row_count, 8, quota_definition.critical_threshold, self.excel.format_wrap)
            row_count += 1

    def close_excel(self):
        self.excel.close_excel()
