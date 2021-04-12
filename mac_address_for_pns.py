from product_info.mac import MAC
import pymongo
import re
from bson import ObjectId

#%%
pn_set = \
    {
        # 271759,
        # 271761,
        # 271762,
        # 301124, # duplicate MAC
        # 301126,
        # 301604,
        # 301605,
        # 304603,
        # 311149,
        # 311183,
        # 311596,
        # 311700,  # TODO
        # 311701,  # TODO
        # 312619,
        # 312646,
        # 321147,
        # 321152,
        # 321181,
        # 321183,
        # 321184,
        # 321185,
        # 322619,
        # 322621,
        # 322623,
        # 322624,
        # 322640,
        # 322646,
        # 322650,
        # 331738,
        # 331739,
        # 331740,
        # 331741,
        # 333019, # TODO: possibly used wrong regx pattern
        # 334669,
        # 335342,
        # 337001,
        # 337009,
        # 337016,
        # 337022,
        # 337025,
        # 337028,
        # 337061,
        # 337082,
        # 337106,
        # 337112,
        # 337118,
        # 337121,
        337122,
        337123,
        337124,
        337125,
        337127,
        337136,
        337139,
        337141,
        337142,
        337143,
        337144,
        337148,
        337172,
        337173,
        337181,
        337183,
        337184,
        337187,
        337190,
        337191,
        337196,
        337199,
        337200,
        337202,
        337205,
        337211,
        337215,
        337217,
        337226,
        337236,
        337238,
        337241,
        337243,
        337247,
        337249,
        337253,
        337256,
        337262,
        337263,
        337271,
        337301,
        337303,
        337307,
        337311,
        337316,
        337318,
        337319,
        337322,
        337325,
        337331,
        337337,
        337346,
        350007,
        350028,
        350029,
        350031,
        350036,
        350037,
        350038,
        350188,
        350201,
        350202,
        350203,
        350205,
        350469,
        350473,
        350505,
        350609,
        350666,
        350791,
        350892,
        350896,
        350899,
        350900,
        350903,
        375700,
        375701,
        375702,
        375704,
        375709,
        375710}

#%%
oid_mac_map = dict()

mac_field_reg = re.compile(r"mac", re.I)

mac_regular_expression = \
 re.compile(r"(?:0040AE|00:40:AE:)?(?!000000|00:00:00|00:40:ae)[0-9a-f]{2}:?[0-9a-f]{2}:?[0-9a-f]{2}(?<!FFFFFF)", re.IGNORECASE)

# mac_regular_expression = \
#     re.compile(r"(?:0040AE|00:40:AE:)?(?!000000|00:00:00|00:40:ae)([0-9a-f]{2}):?"
#                r"([0-9a-f]{2}):?([0-9a-f]{2})(\s|$)", re.IGNORECASE)

collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")["TestMFG"]["TestRecords3"]

cursor = collection.find({"PN": 337122}).sort("Timestamp", -1)

flag = False

for entry in cursor:
    mac_address_list = []
    oid_mac_map[entry['_id']] = {"mac_location": "", "mac_address": "", "serial_number": entry['SerialNumber']}
    # print(entry['_id'])
    for tc in entry["TestResults"]:
        if not flag:
            for parameter in entry['TestResults'][tc]['Test Runs'][0]['Parameters']:
                matching_result = mac_field_reg.search(parameter)
                parameter_detail = entry['TestResults'][tc]['Test Runs'][0]['Parameters'][parameter]['Detail']
                if matching_result:
                    # print(tc)
                    mac_address = entry['TestResults'][tc]['Test Runs'][0]['Parameters'][parameter]['Measured']
                    # print(mac_address)
                    if mac_address == "":
                        print("empty MAC address")
                    elif isinstance(mac_address, list):
                        for address in mac_address:
                            mac_address_list.append(str(MAC(address)))
                    elif mac_address == "FFFFFFFF":
                        print("Invalid MAC FFFFFFFF")
                    else:
                        print(entry['_id'], tc, parameter)
                        try:
                            if isinstance(mac_address, str):
                                mac_address = mac_regular_expression.search(mac_address).group(0)
                            mac_address_list.append(str(MAC(mac_address)))
                        except ValueError as e:
                            print("Invalid MAC address", tc, parameter, mac_address)
                    print("Parameter: ", tc, parameter, entry['SerialNumber'], entry['_id'], mac_address_list)
                    oid_mac_map[entry['_id']]['mac_location'] = "parameter"
                    oid_mac_map[entry['_id']]['mac_address'] = mac_address_list
                    if mac_address_list:
                        flag = True
                if isinstance(parameter_detail, str) and "mac" in parameter_detail.lower():
                    if "exception" in parameter_detail.lower():
                        continue
                    if not flag:
                        mac_address = \
                            mac_regular_expression.findall(entry['TestResults'][tc]['Test Runs'][0]
                                                          ['Parameters'][parameter]['Detail'])
                        if mac_address:
                            for address in mac_address:
                                mac_address_list.append(str(MAC(address)))
                            print("Match Detail: ", tc, parameter, entry['_id'], entry['TestResults'][tc]['Test Runs'][0]
                                                          ['Parameters'][parameter]['Detail'])
                            oid_mac_map[entry['_id']]["mac_location"] = "detail"
                            oid_mac_map[entry['_id']]["mac_address"] = mac_address_list
                            flag = True
                        else:
                            print("No Match Detail: ", tc, parameter, entry['_id'],
                                  # entry['TestResults'][tc]['Test Runs'][0]
                                  # ['Parameters'][parameter]['Detail']
                                  )
    flag = False
    print("---")

oid_with_mac = []
oid_without_mac = []
for oid in oid_mac_map:
    if oid_mac_map[oid]['mac_address']:
        oid_with_mac.append(oid)
        # print(str(oid), oid_mac_map[oid]['serial_number'], oid_mac_map[oid]['mac_address'])
    else:
        oid_without_mac.append(oid)

print(oid_with_mac)

#%%
# first_id = list(oid_mac_map.keys())[0]
# mac_address = oid_mac_map[first_id]['mac_address']
# entry = collection.find({"_id": first_id})[0]
# collection.update_one({"_id": first_id}, {"$set": {"Unique Info.MAC Address": [mac_address]}})

for oid in oid_mac_map:
    mac_address = oid_mac_map[oid]['mac_address']
    doc_entry = collection.find({"_id": oid})[0]
    if not mac_address:
        collection.update_one({"_id": oid}, {"$set": {"Unique Info": {}}})
    else:
        collection.update_one({"_id": oid}, {"$set": {"Unique Info.MAC Address": mac_address}})

