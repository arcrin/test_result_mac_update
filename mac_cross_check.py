#%%
from product_info.serial_number import SerialNumber
from product_info.mac import MAC
from bson import ObjectId
import pymssql
import pymongo


pn_set = \
    [
        # 271759,
        # 271761,
        # 271762,
        # 301124,  # duplicate MAC
        # 301126,
        # 301604,  # mac address assigned to engine
        # 301605,
        # 304603,
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

exception_oid = [
    ObjectId('5df3b9214c3d5fc2ee06c685'),
    ObjectId('5df3bbaad471fb9efdcef718'),
    ObjectId('5df3bc19d471fb9efdcef719'),
    ObjectId('5df3bcc0d471fb9efdcef71b'),
    ObjectId('5df3bd72d471fb9efdcef71d'),
    ObjectId('5df3bdf0d471fb9efdcef71e'),
    ObjectId('5df3be4bd471fb9efdcef71f'),
    ObjectId('5df3c08466570564e4af07f0'),
    ObjectId('5df3c11866570564e4af07f1'),
    ObjectId('5df3c17a66570564e4af07f2'),
    ObjectId('5df3c23566570564e4af07f4'),
    ObjectId('5df3c2c066570564e4af07f5'),
    ObjectId('5df3c3d066570564e4af07f7'),
    ObjectId('5df3c4ad66570564e4af07f9'),
    ObjectId('5df3c53a66570564e4af07fa'),
    ObjectId('5df3c59d66570564e4af07fb'),
    ObjectId('5df3c6c466570564e4af07fc'),
    ObjectId('5df3e4d9666a58d298df6080'),
    ObjectId('5df3e9c3666a58d298df6087'),
    ObjectId('5df3ea2a666a58d298df6088'),
    ObjectId('5df3eec4666a58d298df608e'),
    ObjectId('5e260540464f9e2273a6903c'),
]

# GP SQL Access Information
GP_UserName = 'TestJigGPAccess'
GP_PW = 'Q2WAXjZYo4f59L1PU7fQ'
GP_SERVER = 'SQLAPP.network.com'
GP_DATABASE = 'DELTA'
GP_Driver = ''

DEBUG_UserName = "IRC_Test"
DEBUG_PW = "IRC_Test"
DEBUG_SERVER = "ldickson7VM"
DEBUG_DATABASE = "RMA"



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

debug_rma_conn = pymssql.connect(DEBUG_SERVER, DEBUG_UserName, DEBUG_PW)

mongo_collection = pymongo.MongoClient("mongodb://qa-testmongo.network.com:27017")["TestMFG"]["TestRecords3"]


def find_mac_from_rma(sn, conn):
    cursor = conn.cursor(as_dict=False)

    cursor.execute(_query_mac, int(SerialNumber(sn)))
    macs = sorted([(str(MAC(entry[0])), entry[1]) for entry in cursor.fetchall()])
    return macs


def is_mongo_mac_entry_listed_in_rma(mongo_mac_list, rma_mac_list):
    rma_mac_records = [entry[0] for entry in rma_mac_list]
    for mac in mongo_mac_list:
        if mac not in rma_mac_records:
            return False
    return True


def traverse_subassemblies(top_product_info):
    sub_assembly_sn = set()
    if "SubAssemblies" in top_product_info:
        for entry in top_product_info['SubAssemblies']:
            sub_assembly_sn.add(top_product_info['SubAssemblies'][entry]['SerialNumber'])
            if "SubAssemblies" in top_product_info['SubAssemblies'][entry]:
                lower_sub_assembly_sn = traverse_subassemblies(top_product_info['SubAssemblies'][entry])
                sub_assembly_sn = sub_assembly_sn.union(lower_sub_assembly_sn)
    return sub_assembly_sn



#%%
id_with_mismatched_macs = {"empty_rma_mac": [], "rma_has_more_entry": [], "same_length_different_entry": []}
for pn in [311149]:
    print(pn)
    for mongo_entry in mongo_collection.find({"PN": pn, "Result": True, "Unique Info.MAC Address": {"$exists": True}}).sort("Timestamp", 1):
        if mongo_entry['_id'] not in exception_oid:
            all_available_macs = []
            all_sn = set()
            all_sn.add(mongo_entry['SerialNumber'])
            mongo_mac_address = mongo_entry['Unique Info']['MAC Address']
            sub_assembly_sn = traverse_subassemblies(mongo_entry)
            all_sn = all_sn.union(sub_assembly_sn)
            for sn in all_sn:
                all_available_macs += find_mac_from_rma(sn)



            all_available_macs = sorted(all_available_macs, key=lambda x: x[1])

            print(mongo_entry["_id"], mongo_entry["SerialNumber"], mongo_mac_address, all_available_macs)

            assert is_mongo_mac_entry_listed_in_rma(mongo_mac_address, all_available_macs), mongo_entry['_id']

#%%
oid_to_update = [
    ObjectId("5df3cf85e24d92df745c4174"),
    ObjectId("5df3d009e24d92df745c4175"),
    ObjectId("5df3d0dee24d92df745c4176"),
    ObjectId("5df3d176e24d92df745c4177"),
    ObjectId("5df3d1f5e24d92df745c4178"),
    ObjectId("5df3d30be24d92df745c4179"),
    ObjectId("5df3d520e24d92df745c417c"),
    ObjectId("5df3d592e24d92df745c417d"),
    ObjectId("5df3d653e24d92df745c417e"),
    ObjectId("5df3d7d3e24d92df745c4180"),
    ObjectId("5df3da11666a58d298df606e"),
    ObjectId("5df3db2e666a58d298df6070"),
    ObjectId("5df3dbed666a58d298df6071"),
    ObjectId("5df3dccb666a58d298df6072"),
    ObjectId("5df3ddca666a58d298df6075"),
    ObjectId("5df3e084666a58d298df607a"),
    ObjectId("5df3e25d666a58d298df607c"),
    ObjectId("5df3e399666a58d298df607e"),
    ObjectId("5df3e3fc666a58d298df607f"),
    ObjectId("5df3e539666a58d298df6081"),
    ObjectId("5df3e632666a58d298df6083"),
    ObjectId("5df3e6bd666a58d298df6084"),
    ObjectId("5df3e7d2666a58d298df6085"),
    ObjectId("5df3ec2d666a58d298df6089"),
    ObjectId("5df3ecd0666a58d298df608a"),
    ObjectId("5df3edd3666a58d298df608d"),
]

for oid in oid_to_update:
    print(oid)
    sn = mongo_collection.find_one({"_id": oid})['SerialNumber']
    mac_address = find_mac_from_rma(sn)[0][0]
    mongo_collection.update_one({"_id": oid}, {"$set": {"Unique Info.MAC Address": [mac_address]}})