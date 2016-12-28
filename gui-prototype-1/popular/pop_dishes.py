from pymongo import MongoClient
import pymongo
import numpy
import json
from bson import json_util
from bson.json_util import dumps

client = MongoClient()
db = client["water_footprint"]
collection_recipes = db["recipes_2"]
collection_crop = db["crop_products_aggregated_by_category"]
collection_animal = db["animal_products_category"]

def Update():
    # update amount equals to the sum of three kinds of waterfootprint
    # for i in collection_animal.find():
    #     string = {}
    #     string["amount"]= i["water_footprint_global_average"]["blue"] + i["water_footprint_global_average"]["green"] + i["water_footprint_global_average"]["grey"]
    #     print (string["amount"])
    #     collection_animal.update(i,{"$set":string})
    for i in collection_crop.find():
        crop_string = {}
        if i["global_wf"]["blue"] is None:
            i["global_wf"]["blue"] = 0.0
            crop_string["amount"]= i["global_wf"]["blue"] + i["global_wf"]["green"] + i["global_wf"]["grey"]
            # collection_crop.update(i,{"$set":crop_string})
            # print(1111111)
        crop_string["amount"]= i["global_wf"]["blue"] + i["global_wf"]["green"] + i["global_wf"]["grey"]
        # print(crop_string["amount"])
        crop_string["water_fBootprint_global_average"] = i["global_wf"]
        collection_crop.update(i,{"$set":crop_string})

def pop_dishes(collection):
    count = 0
    pop_list =[]
    # get 10 popular dishes
    fp = open('popular/dishes.json','w+')
    for i in collection.find().sort("rating", pymongo.DESCENDING).limit(10):
        string = {}
        string["name"] = i["recipeName"]
        string["ingredients"] = i["ingredients"]
        pop_list.append(string)
    json.dump(pop_list, fp)
    fp.close()
    return 0

# def Bad_animal_footprint(collection):
#     count = 0
#     bad_list = []
#
#     fp = open('popular/bad_animal.json','w+')
#     for i in collection.find().sort("amount", pymongo.DESCENDING).limit(10):
#         string = {}
#         string["product"] = i["product"]
#         # string["blue"] = i["water_footprint_global_average"]["blue"]
#         # string["green"] = i["water_footprint_global_average"]["green"]
#         # string["grey"] = i["water_footprint_global_average"]["grey"]
#         string["water_footprint_global_average"] = i["water_footprint_global_average"]
#         string["amount"] = i["amount"]
#         bad_list.append(string)
#     json.dump(bad_list, fp)
#     fp.close()
#     return 0

# def Good_animal_footprint(collection):
#     count = 0
#     good_list = []
#
#     fp = open('popular/good_animal.json','w+')
#     for i in collection.find().sort("amount", pymongo.ASCENDING).limit(10):
#         string = {}
#         string["product"] = i["product"]
#         string["water_footprint_global_average"] = i["water_footprint_global_average"]
#         string["amount"] = i["amount"]
#         good_list.append(string)
#     json.dump(good_list, fp)
#     fp.close()
#     return 0

def Bad_crop_footprint(collection):
    count = 0
    bad_list = []

    fp = open('popular/bad_crop.json','w+')
    for i in collection.find().sort("amount", pymongo.DESCENDING).limit(10):
        string = {}
        string["product"] = i["product"]
        # string["water_footprint_global_average"] = i["global_wf"]
        string["blue"] = i["global_wf"]["blue"]
        string["green"] = i["global_wf"]["green"]
        string["grey"] = i["global_wf"]["grey"]
        string["amount"] = i["amount"]
        bad_list.append(string)
    json.dump(bad_list, fp)
    fp.close()
    return 0

def Good_crop_footprint(collection):
    count = 0
    good_list = []

    fp = open('popular/good_crop.json','w+')
    for i in collection.find().sort("amount", pymongo.ASCENDING).limit(10):
        string = {}
        string["product"] = i["product"]
        # string["water_footprint_global_average"] = i["global_wf"]
        string["blue"] = i["global_wf"]["blue"]
        string["green"] = i["global_wf"]["green"]
        string["grey"] = i["global_wf"]["grey"]
        string["amount"] = i["amount"]
        good_list.append(string)
    json.dump(good_list, fp)
    fp.close()
    return 0


def savetxt(filename,x):
    numpy.savetxt(filename,x,fmt='%s',newline='\n')

result_dish = pop_dishes(collection_recipes)
# result_bad_animal = Bad_animal_footprint(collection_animal)
# result_good_animal = Good_animal_footprint(collection_animal)
result_bad_crop = Bad_crop_footprint(collection_crop)
result_good_crop = Good_crop_footprint(collection_crop)
# Update()
