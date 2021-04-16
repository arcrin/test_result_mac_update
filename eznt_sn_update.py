import pymongo


collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")['TestMFG']['TestRecords3']


#%%
filter_dict = {"PN": 337190, "SerialNumber": "114072"}

cursor = collection.find(filter=filter_dict)

oid_sn_map = dict()

for entry in cursor:
    if "Write NFC" in entry['TestResults']:
        oid = entry['_id']
        oid_sn_map[oid] = {'mo': 0, 'sn': 0}
        test_results = entry['TestResults']['Write NFC']['Test Runs'][0]['Parameters']['Updated values']['Measured']['sector3']
        sn = int(test_results['serial'])
        mo = int(test_results['mo'])
        oid_sn_map[oid]['mo'] = mo
        oid_sn_map[oid]['sn'] = sn

for oid in oid_sn_map:
    print(oid, f'{oid_sn_map[oid]["mo"]}/{oid_sn_map[oid]["sn"]:04}')


#%%
for oid in oid_sn_map:
    mo = oid_sn_map[oid]['mo']
    sn = oid_sn_map[oid]['sn']
    collection.update_one({"_id": oid},
                          {"$set": {
                              "MO": mo,
                              "SN": sn,
                              "SerialNumber": f'{mo}/{sn:04}'
                          }})