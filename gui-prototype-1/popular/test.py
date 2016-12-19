from pymongo import MongoClient
import pymongo
import numpy
# import simplejson as json
import json
from bson import json_util
from bson.json_util import dumps

client = MongoClient()
db = client["water_footprint"]
collection_recipes = db["recipes_2"]
collection_crop = db["crop_products_aggregated_by_category"]
collection_animal = db["animal_products_category"]

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
        # count = count + 1
        # print(count)
        # if count >= 10:
        #     break
    json.dump(pop_list, fp)
    fp.close()
    return 0

result_dish = pop_dishes(collection_recipes)
