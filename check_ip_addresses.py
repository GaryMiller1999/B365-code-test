import argparse
import requests
import pprint
import ipaddress
import uuid
import json
import os
import time
from collections import defaultdict


class Main():

    def __init__(self):

        self.argsparse()
        ipaddr = self.args.IPAddress
        ipaddr = ipaddr.split()
        ip_objects = []
        self.guid = uuid.uuid4()

        for i in ipaddr:
            try:
                ip_objects.append(ipaddress.ip_address(i))
            except ValueError as e:
                pprint.pp(
                    f"Unable to parse ip address: {i}, please check your input")
                exit(1)

        response_objs = self.check_ip_in_endpoint(ip_objects, self.guid)
        print(json.dumps(response_objs))
        exit(0)

    def argsparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "IPAddress", help="submit IP addresses space-seperated")
        self.args = parser.parse_args()

    def check_ip_in_endpoint(self, ipaddresses: list, guid: str):
        o365_data = self.retrieve_dataset(guid)
        o365_filtered_data = []
        return_object = []

        for i in ipaddresses:

            for service in o365_data:
                if "ips" in service:
                    for network in service["ips"]:
                        if i in ipaddress.ip_network(network):
                            o365_filtered_data.append(service)
                            break




        # I'm doing this because the data returned from the "endpoints" endpoint matches multiple times on the same IP, e.g. skype, has 4 matches each with different urls and partially different sets of CIDR ranges,
        # because of this I've decided to collapse all of these multi-matched same-service items into one, so the end result will be one list item for each service, instead of say 5 list items, 4 of them being for skype 
        # ane one being for Common.
        
        dd = defaultdict(lambda: defaultdict(list))

        for i in o365_filtered_data:
            for y in i.keys():
                if isinstance(i[y], list):
                    for item in i[y]:
                        dd[i["serviceArea"]][y].append(item)
                else:
                    dd[i["serviceArea"]][y].append(i[y])

        for i in dd.keys():
            for y in dd[i].keys():
                dd[i][y] = list(set(dd[i][y]))

        for i in dd.keys():

            return_object.append(
                {"ServiceGroup": i, "urls": dd[i]["urls"], "cidrs": dd[i]["ips"]})

        return return_object

    def retrieve_dataset(self, guid: str):

        if os.path.exists("./cache"):
            if os.path.getctime("./cache") > (time.time() - 2560):
                # only use the cache if it is less than 1 hour in age, added to reduce excessive polling of the endpoint 1 hour timeframe is arbitrary
                with open("./cache", mode="r") as f:
                    return json.loads(f.read())

        payload = {'ClientRequestId': guid}
        response = requests.get(
            "https://endpoints.office.com/endpoints/worldwide", params=payload)

        if response.status_code != 200:
            print("endpoint repsonded incorrectly and no in-date cache is available.")
            exit(1)

        with open("./cache", mode="w") as f:
            f.write(response.text)
        return json.loads(response.text)


Main()
