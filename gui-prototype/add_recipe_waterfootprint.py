import app
import json
from pymongo import MongoClient
def update():
    connection = MongoClient(app.MONGODB_HOST, app.MONGODB_PORT)
    collection = connection[app.DBS_NAME][app.COLLECTION_RECIPES]
    for i in collection.find({}):
        print(i['recipeName'])
        ingredients = i['ingredients']
        delimiter = ','
        str = delimiter.join(ingredients)
        water = json.loads(app.recipe_waterfootprint(str))
        water["total"] = float(water["blue"])+float(water["green"])+float(water["grey"])
        collection.update({'_id': i['_id']}, {'$set':{'water_footprint': water}})
update()