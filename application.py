import requests
import datetime
import os
import sys
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import xml.dom.minidom


class application(object):
    def __init__(self):
        load_dotenv('.env')
        self.ROOT = os.getenv('ROOT')
        self.TARIFF_SYNC_USERNAME = os.getenv('TARIFF_SYNC_USERNAME')
        self.TARIFF_SYNC_PASSWORD = os.getenv('TARIFF_SYNC_PASSWORD')
        self.create_folders()

    def create_folders(self):
        cwd = os.getcwd()
        self.resources_folder = os.path.join(cwd, "resources")
        if not os.path.exists(self.resources_folder):
            os.mkdir(self.resources_folder)

        self.xml_folder = os.path.join(self.resources_folder, "xml")
        if not os.path.exists(self.xml_folder):
            os.mkdir(self.xml_folder)

        now = datetime.datetime.now()
        for i in range(now.year - 2, now.year + 1):
            year_folder = os.path.join(self.xml_folder, str(i))
            if not os.path.exists(year_folder):
                os.mkdir(year_folder)

    def download(self, year, from_file, to_file):
        for iterator in range(to_file + 1, from_file, -1):
            increment = str(iterator).zfill(3)
            filename = "TGB" + str(year) + increment + ".xml"
            url = self.ROOT + filename
            my_path = os.path.join(self.xml_folder, str(year))
            print(url)
            resp = requests.get(url, auth=HTTPBasicAuth(
                self.TARIFF_SYNC_USERNAME, self.TARIFF_SYNC_PASSWORD))
            if resp.status_code == 200:
                path = os.path.join(my_path, filename)
                if not os.path.exists(path):
                    f = open(path, "w+")
                    dom = xml.dom.minidom.parseString(resp.text)
                    f.write(dom.toprettyxml())
                    f.close()
