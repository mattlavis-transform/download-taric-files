import requests
from datetime import timedelta
from datetime import datetime
import os
from os import system, name, path
import sys
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import xml.dom.minidom

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
            operation = "U"
            self.doprint("Updating " + object_description + " " + str(value))
        elif update_type == "2":  # DELETE
            operation = "D"
            self.doprint("Deleting " + object_description + " " + str(value))
        elif update_type == "3":  # INSERT
            operation = "C"
            self.doprint("Creating " + object_description + " " + str(value))

        return operation

    def num_to_bool(self, num):
        num = int(num)
        if num == 0:
            return False
        else:
            return True
