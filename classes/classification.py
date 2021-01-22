from datetime import datetime
import os
import classes.globals as g


class classification(object):
    def __init__(self, goods_nomenclature_item_id, producline_suffix, number_indents, leaf, significant_digits):
        self.goods_nomenclature_item_id = goods_nomenclature_item_id
        self.productline_suffix = producline_suffix
        self.number_indents = int(number_indents)
        self.leaf = int(leaf)
        self.significant_digits = int(significant_digits)
        self.relations = []
