from classes.database import Database


class Measure(object):
    def __init__(self):
        self.measure_components = []

    def build_duty(self):
        self.duty = ""
        if len(self.measure_components) > 0:
            for mc in self.measure_components:
                mc.build_duty()
                if self.duty != "":
                    if "MAX" not in mc.duty and "MIN" not in mc.duty:
                        self.duty += " + "
                    else:
                        self.duty += " "
                self.duty += mc.duty

        if self.duty == "":
            self.duty = "Variable / EPS"
