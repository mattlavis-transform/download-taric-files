import xml.etree.ElementTree as ET
import sys
import os

from classes.bcolors import bcolors
import classes.globals as g
from models.profile_10000_footnote_type import FootnoteType
from models.profile_10005_footnote_type_description import FootnoteTypeDescription
from models.profile_11000_certificate_type import CertificateType
from models.profile_11005_certificate_type_description import CertificateTypeDescription
from models.profile_12000_additional_code_type import AdditionalCodeType
from models.profile_12005_additional_code_type_description import AdditionalCodeTypeDescription
from models.profile_13000_language import Language
from models.profile_13005_language_description import LanguageDescription
from models.profile_14000_measure_type_series import MeasureTypeSeries
from models.profile_14005_measure_type_series_description import MeasureTypeSeriesDescription
from models.profile_15000_regulation_group import RegulationGroup
from models.profile_15005_regulation_group_description import RegulationGroupDescription
from models.profile_16000_regulation_role_type import RegulationRoleType
from models.profile_16005_regulation_role_type_description import RegulationRoleTypeDescription
from models.profile_17000_publication_sigle import PublicationSigle
from models.profile_20000_footnote import Footnote
from models.profile_20005_footnote_description_period import FootnoteDescriptionPeriod
from models.profile_20010_footnote_description import FootnoteDescription
from models.profile_20500_certificate import Certificate
from models.profile_20505_certificate_description_period import CertificateDescriptionPeriod
from models.profile_20510_certificate_description import CertificateDescription
from models.profile_21000_measurement_unit import MeasurementUnit
from models.profile_21005_measurement_unit_description import MeasurementUnitDescription
from models.profile_21500_measurement_unit_qualifier import MeasurementUnitQualifier
from models.profile_21505_measurement_unit_qualifier_description import MeasurementUnitQualifierDescription
from models.profile_22000_measurement import Measurement
from models.profile_22500_monetary_unit import MonetaryUnit
from models.profile_22505_monetary_unit_description import MonetaryUnitDescription
from models.profile_23000_duty_expression import DutyExpression
from models.profile_23005_duty_expression_description import DutyExpressionDescription
from models.profile_23500_measure_type import MeasureType
from models.profile_23505_measure_type_description import MeasureTypeDescription
from models.profile_24000_additional_code_type_measure_type import AdditionalCodeTypeMeasureType
from models.profile_24500_additional_code import AdditionalCode
from models.profile_24505_additional_code_description_period import AdditionalCodeDescriptionPeriod
from models.profile_24510_additional_code_description import AdditionalCodeDescription
from models.profile_24515_footnote_association_additional_code import FootnoteAssociationAdditionalCode
from models.profile_25000_geographical_area import GeographicalArea
from models.profile_25005_geographical_area_description_period import GeographicalAreaDescriptionPeriod
from models.profile_25010_geographical_area_description import GeographicalAreaDescription
from models.profile_25015_geographical_area_membership import GeographicalAreaMembership
from models.profile_27000_goods_nomenclature_group import GoodsNomenclatureGroup
from models.profile_27005_goods_nomenclature_group_description import GoodsNomenclatureGroupDescription
from models.profile_27500_complete_abrogation_regulation import CompleteAbrogationRegulation
from models.profile_28000_explicit_abrogation_regulation import ExplicitAbrogationRegulation
from models.profile_28500_base_regulation import BaseRegulation
from models.profile_29000_modification_regulation import ModificationRegulation
from models.profile_29500_prorogation_regulation import ProrogationRegulation
from models.profile_29505_prorogation_regulation_action import ProrogationRegulationAction
from models.profile_30000_full_temporary_stop_regulation import FullTemporaryStopRegulation
from models.profile_30005_fts_regulation_action import FtsRegulationAction
from models.profile_30500_regulation_replacement import RegulationReplacement
from models.profile_32000_meursing_table_plan import MeursingTablePlan
from models.profile_32500_meursing_heading import MeursingHeading
from models.profile_32505_meursing_heading_text import MeursingHeadingText
from models.profile_32510_footnote_association_meursing_heading import FootnoteAssociationMeursingHeading
from models.profile_33000_meursing_subheading import MeursingSubheading
from models.profile_34000_meursing_additional_code import MeursingAdditionalCode
from models.profile_34005_meursing_table_cell_component import MeursingTableCellComponent
from models.profile_35000_measure_condition_code import MeasureConditionCode
from models.profile_35005_measure_condition_code_description import MeasureConditionCodeDescription
from models.profile_35500_measure_action import MeasureAction
from models.profile_35505_measure_action_description import MeasureActionDescription
from models.profile_36000_quota_order_number import QuotaOrderNumber
from models.profile_36010_quota_order_number_origin import QuotaOrderNumberOrigin
from models.profile_36015_quota_order_number_origin_exclusion import QuotaOrderNumberOriginExclusion
from models.profile_37000_quota_definition import QuotaDefinition
from models.profile_37005_quota_association import QuotaAssociation
from models.profile_37010_quota_blocking_period import QuotaBlockingPeriod
from models.profile_37015_quota_suspension_period import QuotaSuspensionPeriod
from models.profile_37500_quota_balance_event import QuotaBalanceEvent
from models.profile_37505_quota_unblocking_event import QuotaUnblockingEvent
from models.profile_37510_quota_critical_event import QuotaCriticalEvent
from models.profile_37515_quota_exhaustion_event import QuotaExhaustionEvent
from models.profile_37520_quota_reopening_event import QuotaReopeningEvent
from models.profile_37525_quota_unsuspension_event import QuotaUnsuspensionEvent
from models.profile_37530_quota_closed_and_balance_transferred_event import QuotaClosedAndBalanceTransferredEvent
from models.profile_40000_goods_nomenclature import GoodsNomenclature
from models.profile_40005_goods_nomenclature_indent import GoodsNomenclatureIndent
from models.profile_40010_goods_nomenclature_description_period import GoodsNomenclatureDescriptionPeriod
from models.profile_40015_goods_nomenclature_description import GoodsNomenclatureDescription
from models.profile_40020_footnote_association_goods_nomenclature import FootnoteAssociationGoodsNomenclature
from models.profile_40025_nomenclature_group_membership import NomenclatureGroupMembership
from models.profile_40035_goods_nomenclature_origin import GoodsNomenclatureOrigin
from models.profile_40040_goods_nomenclature_successor import GoodsNomenclatureSuccessor
from models.profile_41000_export_refund_nomenclature import ExportRefundNomenclature
from models.profile_41005_export_refund_nomenclature_indent import ExportRefundNomenclatureIndent
from models.profile_41010_export_refund_nomenclature_description_period import ExportRefundNomenclatureDescriptionPeriod
from models.profile_41015_export_refund_nomenclature_description import ExportRefundNomenclatureDescription
from models.profile_41020_footnote_association_ern import FootnoteAssociationErn
from models.profile_43000_measure import Measure
from models.profile_43005_measure_component import MeasureComponent
from models.profile_43010_measure_condition import MeasureCondition
from models.profile_43011_measure_condition_component import MeasureConditionComponent
from models.profile_43015_measure_excluded_geographical_area import MeasureExcludedGeographicalArea
from models.profile_43020_footnote_association_measure import FootnoteAssociationMeasure
from models.profile_43025_measure_partial_temporary_stop import MeasurePartialTemporaryStop
from models.profile_44000_monetary_exchange_period import MonetaryExchangePeriod
from models.profile_44005_monetary_exchange_rate import MonetaryExchangeRate


class TaricFile(object):
    def __init__(self, taric_filename):
        self.business_rule_violations = []
        self.taric_filename = taric_filename
        sys.exit()

    def parse_xml(self):
        self.duty_measure_list = []

        g.app.print_to_terminal(
            "Preparing to import file " + self.taric_filename + " into database " + g.app.DBASE, False)

        if g.app.prompt:
            ret = g.app.yes_or_no("Do you want to continue?")
            if not (ret) or ret in ("n", "N", "No"):
                sys.exit()

        g.app.load_data_sets_for_validation()
        self.check_already_loaded()
        g.app.create_log_file(self.taric_filename)

        # Load file
        ET.register_namespace('oub', 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0')
        ET.register_namespace('env', 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0')
        try:
            tree = ET.parse(self.taric_filename)
        except:
            print(
                "The selected file could not be found or is not a valid, well-formed XML file")
            sys.exit(0)
        root = tree.getroot()

        for transaction in root.findall('.//env:transaction', g.app.namespaces):
            for message in transaction.findall('.//env:app.message', g.app.namespaces):
                record_code = message.find(".//oub:record.code", g.app.namespaces).text
                sub_record_code = message.find(".//oub:subrecord.code", g.app.namespaces).text
                update_type = message.find(".//oub:update.type", g.app.namespaces).text
                transaction_id = message.find(".//oub:transaction.id", g.app.namespaces).text
                message_id = message.attrib["id"]

                # 10000	FOOTNOTE TYPE
                if record_code == "100" and sub_record_code == "00":
                    o = FootnoteType()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 10000	FOOTNOTE TYPE DESCRIPTION
                if record_code == "100" and sub_record_code == "05":
                    o = FootnoteTypeDescription()
                    o.parse_node(self, update_type, message, transaction_id, message_id, record_code, sub_record_code)

                # 11000	CERTIFICATE TYPE
                if record_code == "110" and sub_record_code == "00":
                    o = CertificateType()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 11005	CERTIFICATE TYPE DESCRIPTION
                if record_code == "110" and sub_record_code == "05":
                    o = CertificateTypeDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 12000	ADDITIONAL CODE TYPE
                if record_code == "120" and sub_record_code == "00":
                    o = AdditionalCodeType()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 12005	ADDITIONAL CODE TYPE DESCRIPTION
                if record_code == "120" and sub_record_code == "05":
                    o = AdditionalCodeTypeDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 13000	LANGUAGE
                if record_code == "130" and sub_record_code == "00":
                    o = Language()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 13005	LANGUAGE DESCRIPTION
                if record_code == "130" and sub_record_code == "05":
                    o = LanguageDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 14000	MEASURE TYPE SERIES
                if record_code == "140" and sub_record_code == "00":
                    o = MeasureTypeSeries()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 14005	MEASURE TYPE SERIES DESCRIPTION
                if record_code == "140" and sub_record_code == "05":
                    o = MeasureTypeSeriesDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 15000	REGULATION GROUP
                if record_code == "150" and sub_record_code == "00":
                    o = RegulationGroup()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 15005	REGULATION GROUP DESCRIPTION
                if record_code == "150" and sub_record_code == "05":
                    o = RegulationGroupDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 16000	REGULATION ROLE TYPE
                if record_code == "160" and sub_record_code == "00":
                    o = RegulationRoleType()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 16005	REGULATION ROLE TYPE DESCRIPTION
                if record_code == "160" and sub_record_code == "05":
                    o = RegulationRoleTypeDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 17000	PUBLICATION SIGLE
                if record_code == "170" and sub_record_code == "00":
                    o = PublicationSigle()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 20000	FOOTNOTE
                if record_code == "200" and sub_record_code == "00":
                    o = Footnote()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 20005	FOOTNOTE DESCRIPTION PERIOD
                if record_code == "200" and sub_record_code == "05":
                    o = FootnoteDescriptionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 20010	FOOTNOTE DESCRIPTION
                if record_code == "200" and sub_record_code == "10":
                    o = FootnoteDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 20500	CERTIFICATE
                if record_code == "205" and sub_record_code == "00":
                    o = Certificate()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 20505	CERTIFICATE DESCRIPTION PERIOD
                if record_code == "205" and sub_record_code == "05":
                    o = CertificateDescriptionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 20510	CERTIFICATE DESCRIPTION
                if record_code == "205" and sub_record_code == "10":
                    o = CertificateDescription()
                    o.parse_node(self, update_type, message, transaction_id, message_id, record_code, sub_record_code)

                # 21000	MEASUREMENT UNIT
                if record_code == "210" and sub_record_code == "00":
                    o = MeasurementUnit()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 21005	MEASUREMENT UNIT DESCRIPTION
                if record_code == "210" and sub_record_code == "05":
                    o = MeasurementUnitDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 21500	MEASUREMENT UNIT QUALIFIER
                if record_code == "215" and sub_record_code == "00":
                    o = MeasurementUnitQualifier()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 21505	MEASUREMENT UNIT QUALIFIER DESCRIPTION
                if record_code == "215" and sub_record_code == "05":
                    o = MeasurementUnitQualifierDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 22000	MEASUREMENT
                if record_code == "220" and sub_record_code == "00":
                    o = Measurement()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 22500	MONETARY UNIT
                if record_code == "225" and sub_record_code == "00":
                    o = MonetaryUnit()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 22500	MONETARY UNIT
                if record_code == "225" and sub_record_code == "05":
                    o = MonetaryUnitDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 23000	DUTY EXPRESSION
                if record_code == "230" and sub_record_code == "00":
                    o = DutyExpression()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 23005	DUTY EXPRESSION DESCRIPTION
                if record_code == "230" and sub_record_code == "05":
                    o = DutyExpressionDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 23500	MEASURE TYPE
                if record_code == "235" and sub_record_code == "00":
                    o = MeasureType()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 23505	MEASURE TYPE DESCRIPTION
                if record_code == "235" and sub_record_code == "05":
                    o = MeasureTypeDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 24000	ADDITIONAL CODE TYPE / MEASURE TYPE
                if record_code == "240" and sub_record_code == "00":
                    o = AdditionalCodeTypeMeasureType()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 24500	ADDITIONAL CODE
                if record_code == "245" and sub_record_code == "00":
                    o = AdditionalCode()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 24505	ADDITIONAL CODE DESCRIPTION PERIOD
                if record_code == "245" and sub_record_code == "05":
                    o = AdditionalCodeDescriptionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 24510	ADDITIONAL CODE DESCRIPTION
                if record_code == "245" and sub_record_code == "10":
                    o = AdditionalCodeDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 24515	FOOTNOTE ASSOCIATION - ADDITIONAL CODE
                if record_code == "245" and sub_record_code == "15":
                    o = FootnoteAssociationAdditionalCode()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 25000	GEOGRAPHICAL AREA
                if record_code == "250" and sub_record_code == "00":
                    o = GeographicalArea()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 25005	GEOGRAPHICAL AREA DESCRIPTION PERIOD
                if record_code == "250" and sub_record_code == "05":
                    o = GeographicalAreaDescriptionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 25010	GEOGRAPHICAL AREA DESCRIPTION
                if record_code == "250" and sub_record_code == "10":
                    o = GeographicalAreaDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 25015	GEOGRAPHICAL AREA MEMBERSHIP
                if record_code == "250" and sub_record_code == "15":
                    o = GeographicalAreaMembership()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 27000	GOODS NOMENCLATURE GROUP
                if record_code == "270" and sub_record_code == "00":
                    o = GoodsNomenclatureGroup()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 27000	GOODS NOMENCLATURE GROUP DESCRIPTION
                if record_code == "270" and sub_record_code == "05":
                    o = GoodsNomenclatureGroupDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 27500	COMPLETE ABROGATION REGULATION
                if record_code == "275" and sub_record_code == "00":
                    o = CompleteAbrogationRegulation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 28000	EXPLICIT ABROGATION REGULATION
                if record_code == "280" and sub_record_code == "00":
                    o = ExplicitAbrogationRegulation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 28500	BASE REGULATION
                if record_code == "285" and sub_record_code == "00":
                    o = BaseRegulation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 29000	MODIFICATION REGULATION
                if record_code == "290" and sub_record_code == "00":
                    o = ModificationRegulation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 29500	PROROGATION REGULATION
                if record_code == "295" and sub_record_code == "00":
                    o = ProrogationRegulation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 29505	PROROGATION REGULATION ACTION
                if record_code == "295" and sub_record_code == "05":
                    o = ProrogationRegulationAction()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 30000	FULL TEMPORARY STOP REGULATION
                if record_code == "300" and sub_record_code == "00":
                    o = FullTemporaryStopRegulation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 30005	FTS REGULATION ACTION
                if record_code == "300" and sub_record_code == "05":
                    o = FtsRegulationAction()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 30500	REGULATION REPLACEMENT
                if record_code == "305" and sub_record_code == "00":
                    o = RegulationReplacement()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 32000	MEURSING TABLE PLAN
                if record_code == "320" and sub_record_code == "00":
                    o = MeursingTablePlan()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 32500	MEURSING HEADING
                if record_code == "325" and sub_record_code == "00":
                    o = MeursingHeading()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 32500	MEURSING HEADING TEXT
                if record_code == "325" and sub_record_code == "05":
                    o = MeursingHeadingText()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 32510	FOOTNOTE ASSOCIATION MEURSING HEADING
                if record_code == "325" and sub_record_code == "10":
                    o = FootnoteAssociationMeursingHeading()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 33000	MEURSING SUBHEADING
                if record_code == "330" and sub_record_code == "00":
                    o = MeursingSubheading()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 34000	MEURSING SUBHEADING
                if record_code == "340" and sub_record_code == "00":
                    o = MeursingAdditionalCode()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 34005	MEURSING TABLE CELL COMPONENT
                if record_code == "340" and sub_record_code == "05":
                    o = MeursingTableCellComponent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 35000	MEASURE CONDITION
                if record_code == "350" and sub_record_code == "00":
                    o = MeasureConditionCode()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 35005	MEASURE CONDITION DESCRIPTION
                if record_code == "350" and sub_record_code == "05":
                    o = MeasureConditionCodeDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 35500	MEASURE ACTION
                if record_code == "355" and sub_record_code == "00":
                    o = MeasureAction()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 35505	MEASURE ACTION DESCRIPTION
                if record_code == "355" and sub_record_code == "05":
                    o = MeasureActionDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 36000	QUOTA ORDER NUMBER
                if record_code == "360" and sub_record_code == "00":
                    o = QuotaOrderNumber()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 36005	QUOTA ORDER NUMBER ORIGIN
                if record_code == "360" and sub_record_code == "10":
                    o = QuotaOrderNumberOrigin()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 36000	QUOTA ORDER NUMBER ORIGIN EXCLUSION
                if record_code == "360" and sub_record_code == "15":
                    o = QuotaOrderNumberOriginExclusion()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37000	QUOTA DEFINITION
                if record_code == "370" and sub_record_code == "00":
                    o = QuotaDefinition()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37005	QUOTA ASSOCIATION
                if record_code == "370" and sub_record_code == "05":
                    o = QuotaAssociation()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37010	QUOTA BLOCKING PERIOD
                if record_code == "370" and sub_record_code == "10":
                    o = QuotaBlockingPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37015	QUOTA SUSPENSION PERIOD
                if record_code == "370" and sub_record_code == "15":
                    o = QuotaSuspensionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37500	QUOTA BALANCE EVENT
                if record_code == "375" and sub_record_code == "00":
                    o = QuotaBalanceEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37505	QUOTA UNBLOCKING EVENT
                if record_code == "375" and sub_record_code == "05":
                    o = QuotaUnblockingEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37510	QUOTA CRITICAL EVENT
                if record_code == "375" and sub_record_code == "10":
                    o = QuotaCriticalEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37515	QUOTA EXHAUSTION EVENT
                if record_code == "375" and sub_record_code == "15":
                    o = QuotaExhaustionEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37520	QUOTA REOPENING EVENT
                if record_code == "375" and sub_record_code == "20":
                    o = QuotaReopeningEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37525	QUOTA UNSUSPENSION EVENT
                if record_code == "375" and sub_record_code == "25":
                    o = QuotaUnsuspensionEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 37530	CLOSED AND BALANCE TRANSFER EVENT
                if record_code == "375" and sub_record_code == "30":
                    o = QuotaClosedAndBalanceTransferredEvent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40000	GOODS NOMENCLATURE
                if record_code == "400" and sub_record_code == "00":
                    o = GoodsNomenclature()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40005	GOODS NOMENCLATURE INDENT
                if record_code == "400" and sub_record_code == "05":
                    o = GoodsNomenclatureIndent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40010	GOODS NOMENCLATURE DESCRIPTION PERIOD
                if record_code == "400" and sub_record_code == "10":
                    o = GoodsNomenclatureDescriptionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40015	GOODS NOMENCLATURE DESCRIPTION
                if record_code == "400" and sub_record_code == "15":
                    o = GoodsNomenclatureDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40020	FOOTNOTE ASSOCIATION GOODS NOMENCLATURE
                if record_code == "400" and sub_record_code == "20":
                    o = FootnoteAssociationGoodsNomenclature()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40025 NOMENCLATURE GROUP MEMBERSHIP
                if record_code == "400" and sub_record_code == "25":
                    o = NomenclatureGroupMembership()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40035	GOODS NOMENCLATURE ORIGIN
                if record_code == "400" and sub_record_code == "35":
                    o = GoodsNomenclatureOrigin()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 40040	GOODS NOMENCLATURE SUCCESSOR
                if record_code == "400" and sub_record_code == "40":
                    o = GoodsNomenclatureSuccessor()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 41000	EXPORT REFUND NOMENCLATURE
                if record_code == "410" and sub_record_code == "00":
                    o = ExportRefundNomenclature()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 41000	EXPORT REFUND NOMENCLATURE INDENT
                if record_code == "410" and sub_record_code == "05":
                    o = ExportRefundNomenclatureIndent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 41000	EXPORT REFUND NOMENCLATURE DESCRIPTION PERIOD
                if record_code == "410" and sub_record_code == "10":
                    o = ExportRefundNomenclatureDescriptionPeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 41000	EXPORT REFUND NOMENCLATURE DESCRIPTION
                if record_code == "410" and sub_record_code == "15":
                    o = ExportRefundNomenclatureDescription()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 41000	FOOTNOTE ASSOCIATION - ERN
                if record_code == "410" and sub_record_code == "20":
                    o = FootnoteAssociationErn()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43000	MEASURE
                if record_code == "430" and sub_record_code == "00":
                    o = Measure()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43005	MEASURE COMPONENT
                if record_code == "430" and sub_record_code == "05":
                    o = MeasureComponent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43010	MEASURE CONDITION
                if record_code == "430" and sub_record_code == "10":
                    o = MeasureCondition()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43011	MEASURE CONDITION COMPONENT
                if record_code == "430" and sub_record_code == "11":
                    o = MeasureConditionComponent()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43015	MEASURE EXCLUDED GEOGRAPHICAL AREA
                if record_code == "430" and sub_record_code == "15":
                    o = MeasureExcludedGeographicalArea()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43020	FOOTNOTE ASSOCIATION - MEASURE
                if record_code == "430" and sub_record_code == "20":
                    o = FootnoteAssociationMeasure()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 43025	MEASURE PARTIAL TEMPORARY STOP
                if record_code == "430" and sub_record_code == "25":
                    o = MeasurePartialTemporaryStop()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 44000	MONETARY EXCHANGE PERIOD
                if record_code == "440" and sub_record_code == "00":
                    o = MonetaryExchangePeriod()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

                # 44005	MONETARY EXCHANGE RATE
                if record_code == "440" and sub_record_code == "05":
                    o = MonetaryExchangeRate()
                    o.parse_node(self, update_type, message, transaction_id,
                                 message_id, record_code, sub_record_code)

