from datetime import timedelta
from datetime import datetime
import os
import json
from os import system, name, path
import sys
from dotenv import load_dotenv
import xml.dom.minidom
from shutil import copyfile
import requests
from requests.auth import HTTPBasicAuth

from classes.database import Database
from classes.classification import Classification
from classes.taric_file import TaricFile


class application(object):
    def __init__(self):
        self.namespaces = {'oub': 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0',
                           'env': 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0', }  # add more as needed
        self.message_count = 0
        load_dotenv('.env')
        self.ROOT = os.getenv('ROOT')
        self.TARIFF_SYNC_USERNAME = os.getenv('TARIFF_SYNC_USERNAME')
        self.TARIFF_SYNC_PASSWORD = os.getenv('TARIFF_SYNC_PASSWORD')
        self.IMPORT_FOLDER = os.getenv('IMPORT_FOLDER')
        self.show_progress = self.num_to_bool(os.getenv('SHOW_PROGRESS'))
        self.create_folders()

    def create_folders(self):
        cwd = os.getcwd()
        self.resources_folder = os.path.join(cwd, "resources")
        if not os.path.exists(self.resources_folder):
            os.mkdir(self.resources_folder)

        paths = ["xml", "xlsx"]
        for path in paths:
            self.sub_folder = os.path.join(self.resources_folder, path)
            if not os.path.exists(self.sub_folder):
                os.mkdir(self.sub_folder)

            now = datetime.now()
            for i in range(now.year - 3, now.year + 1):
                year_folder = os.path.join(self.sub_folder, str(i))
                if not os.path.exists(year_folder):
                    os.mkdir(year_folder)

        self.xml_folder = os.path.join(self.resources_folder, "xml")
        self.xlsx_folder = os.path.join(self.resources_folder, "xlsx")

    def download(self, year, from_file, to_file):
        for iterator in range(to_file + 1, from_file, -1):
            increment = str(iterator).zfill(3)
            filename = "TGB" + str(year)[-2:] + increment + ".xml"
            url = self.ROOT + filename
            my_path = os.path.join(self.xml_folder, str(year))
            print(url)
            resp = requests.get(url, auth=HTTPBasicAuth(self.TARIFF_SYNC_USERNAME, self.TARIFF_SYNC_PASSWORD))
            if resp.status_code == 200:
                path = os.path.join(my_path, filename)
                if not os.path.exists(path):
                    f = open(path, "w+")
                    # This saves and pretty prints the files
                    dom = xml.dom.minidom.parseString(resp.text)
                    f.write(dom.toprettyxml())
                    f.close()

                # Copy to the import folder for running the import
                dest = os.path.join(self.IMPORT_FOLDER, "EU")
                dest = os.path.join(dest, filename)
                copyfile(path, dest)

    def parse(self, year, from_file, to_file):
        for iterator in range(to_file + 1, from_file, -1):
            increment = str(iterator).zfill(3)
            filename = "TGB" + str(year)[-2:] + increment + ".xml"
            my_path = os.path.join(self.xml_folder, str(year))
            path = os.path.join(my_path, filename)
            if os.path.exists(path):
                taric_file = TaricFile(my_path, filename)
                taric_file.parse_xml()
                taric_file.generate_xml()

    def get_timestamp(self):
        ts = datetime.now()
        ts_string = datetime.strftime(ts, "%Y%m%dT%H%M%S")
        return (ts_string)

    def get_datestamp(self):
        ts = datetime.now()
        ts_string = datetime.strftime(ts, "%Y-%m-%d")
        return (ts_string)

    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system("printf '\33c\e[3J'")

    def doprint(self, s):
        if self.show_progress is True:
            print(s)

    def get_value(self, node, xpath, return_null=False):
        try:
            s = node.find(xpath, self.namespaces).text
        except:
            if return_null:
                s = None
            else:
                s = ""
        return (s)

    def get_number_value(self, node, xpath, return_null=False):
        try:
            s = int(node.find(xpath, self.namespaces).text)
        except:
            if return_null:
                s = None
            else:
                s = ""
        return (s)

    def get_node(self, node, xpath):
        try:
            s = node.find(xpath, self.namespaces)
        except:
            s = None
        return (s)

    def get_date_value(self, node, xpath, return_null=False):
        try:
            s = node.find(xpath, self.namespaces).text
            pos = s.find("T")
            if pos > -1:
                s = s[0:pos]
            s = datetime.strptime(s, "%Y-%m-%d")
        except:
            if return_null:
                s = None
            else:
                s = ""
        return (s)

    def get_index(self, node, xpath):
        index = -1
        for child in node.iter():
            index += 1
            s = child.tag.replace(
                "{urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0}", "")
            if s == xpath:
                break
        return index

    def print_to_terminal(self, s, include_indent=True):
        if self.show_progress or include_indent is True:
            if include_indent:
                s = "- " + s
            else:
                s = "\n" + s.upper()
            print(s)

    def get_loading_message(self, update_type, object_description, value):
        operation = ""
        if update_type == "1":  # UPDATE
            operation = "Update "
            self.doprint("Updating " + object_description + " " + str(value))
        elif update_type == "2":  # DELETE
            operation = "Delete "
            self.doprint("Deleting " + object_description + " " + str(value))
        elif update_type == "3":  # INSERT
            operation = "Create "
            self.doprint("Creating " + object_description + " " + str(value))

        return operation

    def num_to_bool(self, num):
        num = int(num)
        if num == 0:
            return False
        else:
            return True

    def format_date(self, d):
        if d is None:
            return ""
        elif d == "":
            return ""
        else:
            return d[8:10] + "/" + d[5:7] + "/" + d[0:4]

    def create_commodity_extract(self, which="eu", date_arg=""):
        if which == "xi":
            which = "eu"
        print("Creating commodity code extract")
        if date_arg == "":
            d = datetime.now()
            d2 = d.strftime('%Y-%m-%d')
        else:
            d2 = date_arg

        self.classifications = []
        # for i in range(7, 8):
        for i in range(0, 10):
            chapter = str(i) + "%"
            sql = "select * from utils.goods_nomenclature_export_new('" + chapter + "', '" + d2 + "') order by 2, 3"
            print("Getting complete commodity code list for codes beginning with " + str(i))
            d = Database(which)
            rows = d.run_query(sql)
            for row in rows:
                self.validity_start_date = str(row[0])
                classification = Classification(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                    row[9],
                    row[10]
                )
                validity_end_date = row[4]
                do_append = True
                if validity_end_date is not None:
                    today = datetime.now()
                    if validity_end_date < today:
                        do_append = False

                if do_append:
                    if classification.leaf:
                        cnt = len(self.classifications)
                        current_indent = classification.number_indents
                        for j in range(cnt - 1, -1, -1):
                            c2 = self.classifications[j]
                            if c2.number_indents < current_indent:
                                classification.hierarchy.append(c2.description)
                                current_indent = c2.number_indents
                            if c2.number_indents == 0:
                                classification.hierarchy.append(c2.description)
                                break

                        # classification.hierarchy = reversed(classification.hierarchy)
                        a = 1

                    self.classifications.append(classification)

        # CSV filename
        path = os.getcwd()
        filename_csv = os.path.join(path, "resources")
        filename_csv = os.path.join(filename_csv, "csv")
        filename_csv = os.path.join(filename_csv, which + "_commodities_" + d2 + ".csv")

        # JSON filename
        filename_json = os.path.join(path, "resources")
        filename_json = os.path.join(filename_json, "json")
        filename_json = os.path.join(filename_json, which + "_commodities_" + d2 + ".json")

        # Write the CSV and the JSON
        f = open(filename_csv, "w+")
        field_names = '"SID","Commodity code","Product line suffix","Start date","End date","Indentation","End line","Description"\n'
        f.write(field_names)

        json_obj = []

        for item in self.classifications:
            f.write(item.extract_row())

            if item.leaf == 1:
                del item.validity_start_date
                del item.validity_end_date
                del item.goods_nomenclature_sid
                del item.productline_suffix
                del item.number_indents
                del item.significant_digits
                del item.chapter
                del item.node

                json_obj.append(item.__dict__)
                a = 1

        f.close()

        # json_data = json.dumps(json_obj.__dict__, lambda o: o.__dict__, indent=4)
        with open(filename_json, 'w') as f:
            json.dump(json_obj, f, indent=4)
