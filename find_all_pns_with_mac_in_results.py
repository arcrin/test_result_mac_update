from bson import ObjectId
import re
import pymongo

collection = pymongo.MongoClient("mongodb://QA-TestMongo.network.com:27017")['TestMFG']['TestRecords3']

mac_field_reg = re.compile(r"mac", re.I)

cursor = collection.find({"_id": ObjectId("5dc0480fe5a5fcf6a1192cb2")})

pn_set = set()

for entry in cursor:
    # print(entry['_id'])
    for tc in entry['TestResults']:
        # print(tc)
        for parameter in entry['TestResults'][tc]['Test Runs'][0]['Parameters']:
            # print(parameter)
            # matching_result = mac_field_reg.match(parameter)
            parameter_detail = entry['TestResults'][tc]['Test Runs'][0]['Parameters'][parameter]['Detail']
            if "mac" in parameter or (isinstance(parameter_detail, str) and "mac" in parameter_detail.lower()):
                print(tc, parameter, entry['_id'])
                pn_set.add(entry['PN'])
            if isinstance(parameter_detail, dict):
                for key in parameter_detail.keys():
                    if "mac" in key.lower():
                        pn_set.add(entry['PN'])
            if isinstance(parameter_detail, list):
                for detail_entry in parameter_detail:
                    if isinstance(detail_entry, str) and "mac" in detail_entry.lower():
                        pn_set.add(entry['PN'])

