import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import xml.dom.minidom


class application(object):
    def __init__(self):
        load_dotenv('.env')
        self.ROOT = os.getenv('ROOT')
        self.TARIFF_SYNC_USERNAME = os.getenv('TARIFF_SYNC_USERNAME')
        self.TARIFF_SYNC_PASSWORD = os.getenv('TARIFF_SYNC_PASSWORD')

    def download(self, year, from_file, to_file):
        for iterator in range(from_file, to_file + 1):
            increment = str(iterator).zfill(3)
            filename = "TGB" + str(year) + increment + ".xml"
            url = self.ROOT + filename
            print(url)
            resp = requests.get(url, auth=HTTPBasicAuth(self.TARIFF_SYNC_USERNAME, self.TARIFF_SYNC_PASSWORD))
            path = "xml/" + filename
            f = open(path, "w+")
            dom = xml.dom.minidom.parseString(resp.text)
            f.write(dom.toprettyxml())
            f.close()
