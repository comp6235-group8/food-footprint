from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import json

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'water_footprint'
#COLLECTION_RECIPES = 'recipies'
COLLECTION_RECIPES = 'recipes_2'
COLLECTION_CROP = 'crop_products_by_category'
COLLECTION_INGREDIENT_TO_WATERFP = 'ingredients_to_recipes'
#FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data/recipies")
def data_recipies():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_RECIPES]

    recipies = collection.distinct("recipeName")
    recipies = sorted(recipies) 
    print "Number of distinct recipies:",len(recipies)

    json_resp = json.dumps(recipies, default=json_util.default)
    connection.close()
    return json_resp

@app.route("/data/ingredients")
def data_ingredients():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    #collection = connection[DBS_NAME][COLLECTION_RECIPIES]
    collection = connection[DBS_NAME][COLLECTION_INGREDIENT_TO_WATERFP]

    #ingredients = collection.distinct("ingredients")
    ingredients = collection.distinct("ingredient")
    ingredients = sorted(ingredients) 
    print "Number of distinct ingredients:",len(ingredients)

    json_resp = json.dumps(ingredients, default=json_util.default)
    connection.close()
    return json_resp

@app.route("/data/wftest")
def data_wftest():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_CROP]

    example = collection.find_one();
    wf = example['water_footprint_global_average']
    list = []
    for key in wf:
        list.append({'name': key, 'value': wf[key]})

    print list    

    json_resp = json.dumps(list, default=json_util.default)
    connection.close()
    return json_resp

# Returns an array with the ingredients of a recipe
@app.route("/data/recipe/ingredients/<recipeName>")
def data_ingredients_per_recipe(recipeName):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_RECIPES]

    print "Processing:", recipeName
    recipe = collection.find_one({"recipeName":recipeName})

    ingredients = []

    if recipe:
        ingredients = recipe['ingredients']

    print "Ingredients:", ingredients

    json_resp = json.dumps(ingredients, default=json_util.default)
    connection.close()
    return json_resp

# Returns the water footprint associated to an ingredient/product
@app.route("/data/ingredient/waterfootprint/<ingredientName>")
def data_waterfootprint_per_ingredient(ingredientName):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_INGREDIENT_TO_WATERFP]
    collection2 = connection[DBS_NAME][COLLECTION_CROP]

    print "Processing:", ingredientName
    ing_wf = collection.find_one({"ingredient":ingredientName})

    waterfootprint = {}

    if ing_wf:
        wf = collection2.find_one({"product_category":ing_wf['product_category'], "product":ing_wf["product"]})
        if wf:
            waterfootprint = wf

    print "Water footprint:", waterfootprint['water_footprint_global_average']

    json_resp = json.dumps(waterfootprint, default=json_util.default)
    connection.close()
    return json_resp

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)