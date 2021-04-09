from bson import ObjectId
import pymongo
import re


mac_regular_expression = \
 re.compile(r"(00:40:AE:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2})", re.IGNORECASE)

collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")["TestMFG"]["TestRecords3"]

cursor = collection.find({"PN": 271761})

for entry in cursor:
    if "Program" in entry['TestResults']:
        # mac address stored in parameter
        # if "MAC address" in entry['TestResults']['Program']['Test Runs'][0]['Parameters']:
            # mac_address = entry['TestResults']['Program']['Test Runs'][0]['Parameters']['MAC address']['Measured']
            # object_id = entry['_id']
            # print(object_id)
            # print(mac_address)
            # collection.update_one({"_id": object_id}, {"$set": {"Unique Info.MAC Address": [mac_address]}})
        # mac address stored in parameter detail
        if "Assign MACs" in entry['TestResults']['Program']['Test Runs'][0]['Parameters']:
            mac_address = entry['TestResults']['Program']['Test Runs'][0]['Parameters']['Assign MACs']['Detail']
            mac_address = mac_regular_expression.search(mac_address, re.IGNORECASE|re.UNICODE).group(0)
            object_id = entry['_id']
            print(object_id)
            print(mac_address)
            collection.update_one({"_id": object_id}, {"$set": {"Unique Info.MAC Address": [mac_address]}})

