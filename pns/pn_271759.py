from bson import ObjectId
import pymongo


collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")["TestMFG"]["TestRecords3"]

cursor = collection.find({"PN": 271759})

for entry in cursor:
    if "Program" in entry['TestResults']:
        if "MAC address" in entry['TestResults']['Program']['Test Runs'][0]['Parameters']:
            mac_address = entry['TestResults']['Program']['Test Runs'][0]['Parameters']['MAC address']['Measured']
            object_id = entry['_id']
            print(entry['_id'])
            print(mac_address)
            collection.update_one({"_id": object_id}, {"$unset": {"Unique Info": ""}})
            collection.update_one({"_id": object_id}, {"$set": {"Unique Info.MAC Address": [mac_address]}})
