from datetime import datetime
import os
import classes.globals as g


class Classification(object):
    def __init__(self, goods_nomenclature_sid, goods_nomenclature_item_id, productline_suffix, validity_start_date, validity_end_date, description, number_indents, chapter, node, leaf, significant_digits):
        self.goods_nomenclature_sid = goods_nomenclature_sid
        self.goods_nomenclature_item_id = goods_nomenclature_item_id
        self.productline_suffix = productline_suffix
        self.validity_start_date = validity_start_date
        self.validity_end_date = validity_end_date
        self.number_indents = int(number_indents)
        self.leaf = int(leaf)
        self.significant_digits = int(significant_digits)
        self.description = description
        self.chapter = chapter
        self.node = node
        if self.goods_nomenclature_item_id == "7606122090":
            a = 1
        if self.validity_end_date is None:
            self.validity_end_date = ""
        self.format_description(add_dashes=False)
        self.hierarchy = []

    def format_description(self, add_dashes=False):
        if self.description is None:
            print("Blank description found on comm code " + self.goods_nomenclature_item_id)
            self.description = ""
        self.description = self.description.replace("|", " ")
        if add_dashes:
            self.description = "- " * self.number_indents + self.description

    def extract_row(self):
        C = ','
        Q = '"'
        CQ = ',"'
        QC = '",'
        NL = "\n"
        s = str(self.goods_nomenclature_sid) + C
        s += Q + self.goods_nomenclature_item_id + QC
        s += Q + self.productline_suffix + QC
        s += Q + g.app.format_date(str(self.validity_start_date)) + QC
        s += Q + g.app.format_date(str(self.validity_end_date)) + QC
        s += str(self.number_indents) + C
        s += str(self.leaf) + C
        s += Q + self.description + Q + NL
        return s

    def extract_json(self):
        return (":sifjso")
    
    # def __iter__(self):
    #     yield 'goods_nomenclature_item_id', self.goods_nomenclature_item_id
        