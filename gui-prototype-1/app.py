from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import json
import numpy

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'water_footprint'
#COLLECTION_RECIPIES = 'recipies'
#COLLECTION_CROP = 'crop_products'
COLLECTION_CROP_AGGREGATED = 'crop_products_aggregated_by_category'
#COLLECTION_RECIPES = 'recipies'
COLLECTION_RECIPES = 'recipes_2'
COLLECTION_CROP = 'crop_products_by_category'
COLLECTION_INGREDIENT_TO_WATERFP = 'ingredient_to_waterfootprint'
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

@app.route("/data/recipes/<name>")
def get_recipes_by_name(name):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_RECIPES]

    recipes = collection.find({"recipeName": {"$regex": u"" + name}}).distinct("recipeName")

    json_resp = json.dumps(recipes)
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

@app.route("/map/ingredient/<name>")
def get_ingredient(name):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_CROP_AGGREGATED]

    product = collection.find_one({"product": name})
    countries = product["countries"]

    json_resp = json.dumps(countries)
    connection.close()
    return json_resp

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

# Returns an array with the ingredients of a recipe
@app.route("/data/recipe/ingredients/<recipeName>")
def data_ingredients_per_recipe(recipeName):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_RECIPES]

    print "Processing:", recipeName
    recipe = collection.find_one({"recipeName": recipeName})

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

    # print "Water footprint:", waterfootprint['water_footprint_global_average']

    json_resp = json.dumps(waterfootprint, default=json_util.default)
    connection.close()
    return json_resp

# Returns the GLOBAL AVERAGE water footprint associated to an ingredient/product
@app.route("/data/ingredient/globalwaterfootprint/<ingredientName>")
def data_globalwaterfootprint_per_ingredient(ingredientName):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_INGREDIENT_TO_WATERFP]
    collection2 = connection[DBS_NAME][COLLECTION_CROP]

    print "Processing:", ingredientName
    ing_wf = collection.find_one({"ingredient":ingredientName})

    waterfootprint = {}

    if ing_wf:
        wf = collection2.find_one({"product_category":ing_wf['product_category'], "product":ing_wf["product"]})
        if wf:
            waterfootprint = wf['water_footprint_global_average']

    # print "Water footprint:", waterfootprint['water_footprint_global_average']

    json_resp = json.dumps(waterfootprint, default=json_util.default)
    connection.close()
    return json_resp

@app.route("/data/wftest")
def data_wftest():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_CROP]

    example = collection.find_one();
    wf = example['water_footprint_global_average']
    #list = []
    #for key in wf:
    #    list.append({'name': key, 'value': wf[key]})

    #print list

    json_resp = json.dumps(wf, default=json_util.default)
    connection.close()
    return json_resp

# Returns the Global Water Footprint (Agreggated from all the products)
@app.route("/data/ingredient/globalwaterfootprint")
def data_globalwaterfootprint():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_CROP]

    aggregation = collection.aggregate([ {
        '$group': {
            '_id': None,
            'totalBlue': {'$sum': '$water_footprint_global_average.blue'},
            'totalGreen': {'$sum': '$water_footprint_global_average.green'},
            'totalGrey': {'$sum': '$water_footprint_global_average.grey'},
            'avgBlue': {'$avg': '$water_footprint_global_average.blue'},
            'avgGreen': {'$avg': '$water_footprint_global_average.green'},
            'avgGrey': {'$avg': '$water_footprint_global_average.grey'}
        } } ] )

    print aggregation['result'];

    water_footprint = {}
    if aggregation['ok'] == 1:
        #water_footprint['blue'] = aggregation['result'][0]['totalBlue']
        #water_footprint['green'] = aggregation['result'][0]['totalGreen']
        #water_footprint['grey'] = aggregation['result'][0]['totalGrey']
        water_footprint['blue'] = aggregation['result'][0]['avgBlue']
        water_footprint['green'] = aggregation['result'][0]['avgGreen']
        water_footprint['grey'] = aggregation['result'][0]['avgGrey']

    return json.dumps(water_footprint)


    connection.close()

# Gets the average water footprints for a recipe
@app.route("/data/recipe/waterfootprint/<ingredients>")
def recipe_waterfootprint(ingredients):
    water_footprints_acc = {"blue": [], "green": [], "grey": []}
    ingredients = ingredients.split(",")
    for ingredient in ingredients:
        water_footprint = json.loads(data_waterfootprint_per_ingredient(ingredient))
        if "water_footprint_global_average" in water_footprint:
            for footprint_type in ["blue", "green", "grey"]:
                if water_footprint["water_footprint_global_average"][footprint_type]:
                    water_footprints_acc[footprint_type].append(water_footprint["water_footprint_global_average"][footprint_type])

    water_footprints = {}
    for footprint_type in ["blue", "green", "grey"]:
        water_footprints[footprint_type] = numpy.mean(water_footprints_acc[footprint_type])

    def list_of_footprints(fp):
        water_footprint_list = []
        for fp_type in ["blue", "green", "grey"]:
            water_footprint_list.append({"name": fp_type, "value": fp[fp_type]})
        return water_footprint_list

    return json.dumps(list_of_footprints(water_footprints))

# Return the waterfootprint of top 10 ingredients
@app.route("/data/top_ingredients/waterfootprint/<ingredients>")
def ingredient_waterfootprint(ingredients):
    ingredients_waterfootprint = []
    ingredients = ingredients.split(",")
    for ingredient in ingredients:
        waterfootprint = json.loads(data_globalwaterfootprint_per_ingredient(ingredient))
        waterfootprint["product"] = ingredient
        ingredients_waterfootprint.append(waterfootprint)
    print ingredients
    return json.dumps(ingredients_waterfootprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
