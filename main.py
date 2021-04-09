import pymongo

#%% Set up
collection = pymongo.MongoClient("mongodb://QA-TestMongo.network.com:27017")['TestMFG']['TestRecords3']

pn_set = \
    {271759,
     271761,
     271762,
     301124,
     301126,
     301604,
     301605,
     304603,
     311149,
     311183,
     311596,
     311601,
     311602,
     311700,
     311701,
     312619,
     312646,
     321146,
     321147,
     321148,
     321152,
     321180,
     321181,
     321183,
     321184,
     321185,
     321600,
     322615,
     322616,
     322619,
     322620,
     322621,
     322623,
     322624,
     322640,
     322642,
     # 322643,
     322646,
     322650,
     323053,
     323054,
     323230,
     331730,
     331731,
     331732,
     331733,
     331734,
     331735,
     331738,
     331739,
     331740,
     331741,
     333007,
     333019,
     # 334669,
     335342,
     335827,
     335881,
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
for pn in pn_set:
    cursor = collection.find({"PN": pn})
    for entry in cursor:
        for tc in entry['TestResults']:
            for parameter in entry['TestResults'][tc]['Test Runs'][0]['Parameters']:
                parameter_detail = entry['TestResults'][tc]['Test Runs'][0]['Parameters'][parameter]['Detail']
                if isinstance(parameter_detail, list):
                    print(entry['_id'], tc)
                    print("Parameter detail stored as list")
                    break