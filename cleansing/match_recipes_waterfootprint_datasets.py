from pymongo import MongoClient
#from bson import json_util
#from bson.json_util import dumps
#import json

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'water_footprint'
COLLECTION_RECIPES = 'recipies'
COLLECTION_RECIPES_2 = 'recipies_2'
COLLECTION_CROP = 'crop_products_by_category'
INGREDIENT_TO_RECIPES_2 = 'recipies_2'

def analyse_problem():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collRecipies = connection[DBS_NAME][COLLECTION_RECIPIES]
    collCrop = connection[DBS_NAME][COLLECTION_CROP]

    #Method:
    #Iterate over the recipies collection
    #For each recipe check if at least one ingredient is linked with a water footprint document
    ingredientsVisited = dict() # Buffer that stores checked ingredients to avoid repeating the search

    # Iterate over recipes
    recipiesCursor = collRecipies.find()
    i = 0
    countNF = 0
    for recipe in recipiesCursor:
        ingredients = recipe['ingredients']

        for ing in ingredients:
            # Check if the ingredient was already analysed
            if ing in ingredientsVisited:
                continue

            print 'Searching water footprint for ingredient:', ing
            waterfpCursor = collCrop.find({'product': { '$regex': ing, '$options': 'i' }});

            if waterfpCursor.count()>0:
                #for doc in cursorWf:
                #    print doc['product']
                print 'Matches:', waterfpCursor.count()
                ingredientsVisited[ing]=1
            else:
                print 'Nothing'
                ingredientsVisited[ing]=0

        #Stop condition
        i = i+1
        #if i >= 100:
        #    break
    connection.close()

    print 'Matches Summary:'
    countMatches = 0
    countNoMatches = 0
    found = []
    notfound = []
    for k in ingredientsVisited:
        if ingredientsVisited[k] == 1:
            found.append(k);
            countMatches = countMatches + 1
        else:
            notfound.append(k);
            countNoMatches = countNoMatches + 1
       
    print 'Matches:'
    print countMatches,'/',len(ingredientsVisited)
    print found
    print 'Without match:'
    print countNoMatches,'/',len(ingredientsVisited)
    print notfound


# Creates a copy of the recipes collection
# but filtering the recipes that contains ingredients
# where at least one ingredient has a match in the water footprint dataset
def createNewCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collRecipes = connection[DBS_NAME][COLLECTION_RECIPES]
    collCrop = connection[DBS_NAME][COLLECTION_CROP]
    collRecipes2 = connection[DBS_NAME][COLLECTION_RECIPES_2]

    # Drop copy table (if exists)
    if COLLECTION_RECIPES_2 in connection[DBS_NAME].collection_names(): #Check if collection exists in db
        if collRecipes2.count() > 0: #Check if collection is empty
            print 'Droping old collection...'
            collRecipes2.drop() #Delete(drop) collection named from db


    #Method:
    #Iterate over the recipies collection
    #For each recipe check if at least one ingredient is linked with a water footprint document (crop or animal)
    ingredientsVisited = dict() # Dict that stores checked ingredients to avoid repeating the search

    # Iterate over recipes
    recipiesCursor = collRecipes.find()
    for recipe in recipiesCursor:
        print 'Searching water footprint for ingredients of the recipe:', recipe['recipeName']
        processed = False

        # Iterate over ingredients of the recipe
        ingredients = recipe['ingredients']
        i = 0
        for ing in ingredients:
            # Check if the ingredient was already analysed
            if ing in ingredientsVisited and ingredientsVisited[ing] == 1:
                print 'Duplicating...'
                collRecipes2.insert(recipe)
                break
            elif ing in ingredientsVisited and ingredientsVisited[ing] == 0:
                continue

            # Search for a match in the crop dataset
            #print 'Searching water footprint for ingredient:', ing
            waterfpCursor = collCrop.find({'product': { '$regex': ing, '$options': 'i' }});

            if waterfpCursor.count()>0:
                # Match!
                #print 'Matches:', waterfpCursor.count()
                ingredientsVisited[ing]=1
                print 'Duplicating...'
                collRecipes2.insert(recipe)
                # Create joining record
                if waterfpCursor.count() == 0:
                    break; #No need to search in the other ingredients
                else:
                    # TODO: Evaluate which match is the best option 
                    break;
            else:
                # No match!
                #print 'Nothing'
                ingredientsVisited[ing]=0

        #Stop condition
        i = i+1
        if i >= 1000:
            break
    connection.close()

    print 'Matches Summary:'
    countMatches = 0
    countNoMatches = 0
    found = []
    notfound = []
    for k in ingredientsVisited:
        if ingredientsVisited[k] == 1:
            found.append(k);
            countMatches = countMatches + 1
        else:
            notfound.append(k);
            countNoMatches = countNoMatches + 1
       
    print 'Matches:'
    print countMatches,'/',len(ingredientsVisited)
    #print found
    print 'Without match:'
    print countNoMatches,'/',len(ingredientsVisited)
    #print notfound


def clean_ingredients():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collRecipies = connection[DBS_NAME][COLLECTION_RECIPES]
    collCrop = connection[DBS_NAME][COLLECTION_CROP]

    #Method:
    #Iterate over the recipies collection
    #For each recipe check if at least one ingredient is linked with a water footprint document

    recipies = collRecipies.find()
 
    i = 0
    countNF = 0
    for r in recipies:
        ingredients = r['ingredients']

        for ing in ingredients:
            print 'Searching wf for ingredient:', ing
            #listWf = collCrop.find({'product': re.compile('product', re.IGNORECASE)})
            #{ $regex: /pattern/, $options: '<options>' }
            cursorWf = collCrop.find({'product': { '$regex': 'tomato', '$options': 'i' }});

            if cursorWf.count()>0:
                for doc in cursorWf:
                    print doc['product']
            else:
                print 'Nothing'

        #Stop condition
        i = i+1
        if i >= 10:
            break
    connection.close()

def data_ingredients():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_RECIPIES]

    ingredients = collection.distinct("ingredients")
    ingredients = sorted(ingredients[0:1000]) # To avoid the big query and on-client processing time. TODO: Improve it
    print "Number of distinct ingredients:",len(ingredients)

    json_resp = json.dumps(ingredients, default=json_util.default)
    connection.close()

def data_wftest():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_CROP]

    example = collection.find_one();
    wf = example['water_footprint_global_average']
    list = []
    for key in wf:
        list.append({'name': key, 'value': wf[key]})

    print list    

    connection.close()




# Run 
#analyse_problem()
createNewCollection();