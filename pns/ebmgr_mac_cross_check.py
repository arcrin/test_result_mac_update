#%%
from product_info.serial_number import SerialNumber
from product_info.mac import MAC
import pymssql
import pymongo


# GP SQL Access Information
GP_UserName = 'TestJigGPAccess'
GP_PW = 'Q2WAXjZYo4f59L1PU7fQ'
GP_SERVER = 'SQLAPP.network.com'
GP_DATABASE = 'DELTA'
GP_Driver = ''

_query_mac = """
    select
        MACAddress, DateUsed
    from
        RMA.dbo.mfgMacAddresses
    where
        SerialNumber=%s
    order by
        MACAddress desc
"""

rma_connection = pymssql.connect(GP_SERVER, GP_UserName, GP_PW, GP_DATABASE)

mongo_collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")["TestMFG"]["TestRecords3"]


def find_mac_from_rma(sn):
    cursor = rma_connection.cursor(as_dict=False)

    cursor.execute(_query_mac, int(SerialNumber(sn)))
    macs = sorted([(str(MAC(entry[0])), entry[1]) for entry in cursor.fetchall()])
    return macs


def is_mongo_mac_entry_listed_in_rma(mongo_mac_list, rma_mac_list):
    rma_mac_records = [entry[0] for entry in rma_mac_list]
    for mac in mongo_mac_list:
        if mac not in rma_mac_records:
            return False
    return True


#%%
id_with_mismatched_macs = {"empty_rma_mac": [], "rma_has_more_entry": [], "same_length_different_entry": []}
sn_with_matched_mac = set()
for pn in [301604]:
    print(pn)
    for mongo_entry in mongo_collection.find({"PN": pn, "Result": True, "Unique Info.MAC Address": {"$exists": True}}).sort("Timestamp", 1):
        all_available_macs = []
        mongo_mac_address = mongo_entry['Unique Info']['MAC Address']
        try:
            engine_sn = mongo_entry['SubAssemblies']["350665"]['SubAssemblies']["350505"]['SerialNumber']
            rma_subassembly_mac_address = find_mac_from_rma(engine_sn)
        except KeyError:
            engine_sn = mongo_entry['SubAssemblies']["350505"]["SerialNumber"]
            rma_subassembly_mac_address = find_mac_from_rma(engine_sn)

        product_sn = mongo_entry['SerialNumber']
        rma_product_mac_address = find_mac_from_rma(product_sn)
        all_available_macs += rma_subassembly_mac_address + rma_product_mac_address
        all_available_macs = sorted(all_available_macs, key=lambda x: x[1])

        print(mongo_entry["_id"], mongo_entry["SerialNumber"], engine_sn, mongo_mac_address, all_available_macs)

        assert is_mongo_mac_entry_listed_in_rma(mongo_mac_address, all_available_macs), mongo_entry['_id']

        # if not rma_mac_address:
        #     id_with_mismatched_macs['empty_rma_mac'].append(mongo_entry['_id'])
        # elif len(rma_mac_address) > len(mongo_mac_address):
        #     id_with_mismatched_macs['rma_has_more_entry'].append(mongo_entry['_id'])
        # else:
        #     id_with_mismatched_macs['same_length_different_entry'].append(mongo_entry['_id'])
        #     assert rma_mac_address == mongo_mac_address, mongo_entry['_id']
