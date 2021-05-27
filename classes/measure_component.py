from classes.database import Database


class MeasureComponent(object):
    def __init__(self):
        self.measure_sid = None
        self.duty_expression_id = None
        self.duty_amount = None
        self.monetary_unit_code = None
        self.measurement_unit_code = None
        self.measurement_unit_qualifier_code = None

    def build_duty(self):
        basics = ["01", "04", "19", "20"]
        maximums = ["17", "35"]
        minimums = ["15"]
        self.duty = ""
        if self.duty_expression_id in maximums:
            self.duty += "MAX "
        elif self.duty_expression_id in minimums:
            self.duty += "MIN "
        elif self.duty_expression_id == "12":
            self.duty = "agricultural component"
            return
        elif self.duty_expression_id == "14":
            self.duty = "reduced agricultural component"
            return
        elif self.duty_expression_id == "21":
            self.duty = "sugar duty"
            return
        elif self.duty_expression_id == "25":
            self.duty = "reduced sugar duty"
            return
        elif self.duty_expression_id == "27":
            self.duty = "flour duty"
            return
        elif self.duty_expression_id == "29":
            self.duty = "reduced flour duty"
            return
        
        if self.measurement_unit_code is None:
            self.duty += "{:,.2f}".format(self.duty_amount) + "%"
        else:
            self.duty += self.monetary_unit_code + " " + "{:,.2f}".format(self.duty_amount) + " / " + self.measurement_unit_code
            if self.measurement_unit_qualifier_code is not None:
                self.duty += " " + self.measurement_unit_qualifier_code
