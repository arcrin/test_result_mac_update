#%%
from product_info.serial_number import SerialNumber
from product_info.mac import MAC
import pymssql
import pymongo

pn_set = \
    [
        # 271759,
        # 271761,
        271762,
        301124, # duplicate MAC
        301126,
        301604,
        301605,
        304603,
        311149,
        311183,
        311596,
        311700,  # TODO
        311701,  # TODO
        312619,
        312646,
        321147,
        321152,
        321181,
        321183,
        321184,
        321185,
        322619,
        322621,
        322623,
        322624,
        322640,
        322646,
        322650,
        331738,
        331739,
        331740,
        331741,
        333019, # TODO: possibly used wrong regx pattern
        334669, # start of eznt
        335342,
        337001,
        337009,
        337016,
        337022,
        337025,
        337028,
        337061,
        337082,
        337106,
        337112,
        337118,
        337121,
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
        337202, # anomoly 5e28c3d7c0eaeba74afb9d33
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
        350037,
        350038,
        350205,
        350666, # skip chip id test case
        350791,
        350892,
        350896,
        350899,
        350900,
        350903,
    ]

# GP SQL Access Information
GP_UserName = 'TestJigGPAccess'
GP_PW = 'Q2WAXjZYo4f59L1PU7fQ'
GP_SERVER = 'SQLAPP.network.com'
GP_DATABASE = 'DELTA'
GP_Driver = ''

_query_mac = """
    select
        MACAddress
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
    macs = sorted([str(MAC(entry[0])) for entry in cursor.fetchall()])
    return macs


def is_mongo_mac_entry_listed_in_rma(mongo_mac_list, rma_mac_list):
    for mac in mongo_mac_list:
        if mac not in rma_mac_list:
            return False
    return True


#%%
id_with_mismatched_macs = {"empty_rma_mac": [], "rma_has_more_entry": [], "same_length_different_entry": []}
for pn in [301124]:
    print(pn)
    for mongo_entry in mongo_collection.find({"PN": pn, "Unique Info.MAC Address": {"$exists": True}}):
        mongo_mac_address = mongo_entry['Unique Info']['MAC Address']
        rma_mac_address = find_mac_from_rma(mongo_entry['SerialNumber'])
        print(mongo_entry["_id"], mongo_entry["SerialNumber"], rma_mac_address, mongo_mac_address)
        # if not rma_mac_address:
        #     id_with_mismatched_macs['empty_rma_mac'].append(mongo_entry['_id'])
        # elif len(rma_mac_address) > len(mongo_mac_address):
        #     id_with_mismatched_macs['rma_has_more_entry'].append(mongo_entry['_id'])
        # else:
        #     id_with_mismatched_macs['same_length_different_entry'].append(mongo_entry['_id'])
        #     assert rma_mac_address == mongo_mac_address, mongo_entry['_id']
