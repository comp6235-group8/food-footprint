from pymongo import MongoClient
#from bson import json_util
#from bson.json_util import dumps
#import json

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'water_footprint'
COLLECTION_RECIPES = 'recipes'
COLLECTION_RECIPES_2 = 'recipes_2'
COLLECTION_CROP = 'crop_products_by_category'
COLLECTION_ANIMAL = 'animal_products_category'
COLLECTION_INGREDIENT_TO_WATERFP = 'ingredient_to_waterfootprint'

# Creates a copy of the recipes collection
# but filtering the recipes that contains ingredients
# where at least one ingredient has a match in the water footprint dataset
def createNewCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collRecipes = connection[DBS_NAME][COLLECTION_RECIPES]
    collCrop = connection[DBS_NAME][COLLECTION_CROP]
    collAnimal = connection[DBS_NAME][COLLECTION_ANIMAL]
    collRecipes2 = connection[DBS_NAME][COLLECTION_RECIPES_2]
    collJoin = connection[DBS_NAME][COLLECTION_INGREDIENT_TO_WATERFP]

    # Drop copy-table and join-table (if exists)
    if COLLECTION_RECIPES_2 in connection[DBS_NAME].collection_names(): #Check if collection exists in db
        if collRecipes2.count() > 0: #Check if collection is not empty
            print 'Droping old collection...'
            collRecipes2.drop() #Delete(drop) collection named from db
    if COLLECTION_INGREDIENT_TO_WATERFP in connection[DBS_NAME].collection_names(): #Check if collection exists in db
        if collJoin.count() > 0: #Check if collection is not empty
            print 'Droping old collection...'
            collJoin.drop() #Delete(drop) collection named from db


    #Method:
    #Iterate over the recipies collection
    #For each recipe check if at least one ingredient is linked with a water footprint document (crop or animal)
    ingredientsVisited = dict() # Dict that stores checked ingredients to avoid repeating the search

    # Iterate over recipes
    i = 0
    copyDataset = []
    recipiesCursor = collRecipes.find()

    for recipe in recipiesCursor:
        print 'Searching water footprint for ingredients of the recipe:', recipe['recipeName']
        duplicate = False

        # Iterate over ingredients of the recipe
        ingredients = recipe['ingredients']
        for ing in ingredients:
            # Check if the ingredient was already analysed
            if ing in ingredientsVisited and ingredientsVisited[ing] == 1:
                duplicate = True
                continue
            elif ing in ingredientsVisited and ingredientsVisited[ing] == 0:
                continue

            # Search for a match in the crop dataset
            # 1) Full coincidence - No case sensitive
            if findMatch(collCrop, ing, ing, ingredientsVisited):
                duplicate = True
                continue
            
            # 2) Two words ingredients -> Ignore first word -> Maybe it is an adjective
            words = ing.split(' ')
            if len(words) == 2:
                if findMatch(collCrop, ing, words[1], ingredientsVisited):
                    duplicate = True
                    continue
            elif len(words) == 3:
                if findMatch(collCrop, ing, words[2], ingredientsVisited):
                    duplicate = True
                    continue
            # elif len(words) > 3:
            #     # 2) Search a match per each word
            #     for word in words:
            #         if findMatch(collCrop, ing, word, ingredientsVisited):
            #             duplicate = True
            #             continue

            #     if duplicate:
            #         continue

            # No match in any of the datasets!
            ingredientsVisited[ing]=0


        if duplicate:
            #Duplicate the recipe if the conditions were met
            #print 'Duplicating...'
            copyDataset.append(recipe)
        else:
            print 'Discarded...'

        #Stop condition
        # i = i+1
        # if i >= 1000:
        #     break

    if len(copyDataset) > 0:
        collRecipes2.insert(copyDataset)

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

def createJoinDocument(ingredientName, product_category, product):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collJoin = connection[DBS_NAME][COLLECTION_INGREDIENT_TO_WATERFP]
    collJoin.insert({'ingredient': ingredientName, 'product_category':product_category, 'product':product})
    connection.close()

def findMatch(collection, ingredient, searchText, ingredientsVisited):
    found=False
    waterfpCursor = collection.find({'product': { '$regex': searchText, '$options': 'i' }});
    
    if waterfpCursor.count()>0:
        # Match!
        ingredientsVisited[ingredient]=1
        found=True

        # Create joining record
        if waterfpCursor.count() == 0:
            createJoinDocument(ingredient, waterfpCursor[0]['product_category'], waterfpCursor[0]['product'])
        else:
            print 'Warning: More than one match for ingredient:',ingredient, searchText
            createJoinDocument(ingredient, waterfpCursor[0]['product_category'], waterfpCursor[0]['product'])

    return found


def analyse_problem():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collRecipes = connection[DBS_NAME][COLLECTION_RECIPES]
    collCrop = connection[DBS_NAME][COLLECTION_CROP]

    #Method:
    #Iterate over the recipies collection
    #For each recipe check if at least one ingredient is linked with a water footprint document
    ingredientsVisited = dict() # Buffer that stores checked ingredients to avoid repeating the search

    # Iterate over recipes
    recipiesCursor = collRecipes.find()
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

    # Check two words ingredients without match:
    print 'Two-words Ingredients without match:'
    for k in ingredientsVisited:
        if ingredientsVisited[k] == 0:
            print k    


def analyze_ingredients():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collRecipes = connection[DBS_NAME][COLLECTION_RECIPES]

    # Iterate over recipes
    ingredientsVisited = []
    recipiesCursor = collRecipes.find()

    for recipe in recipiesCursor:
        ingredients = recipe['ingredients']

        for ing in ingredients:
            # Check if the ingredient was already analysed
            if ing in ingredientsVisited:
                continue


            ingredientsVisited.append(ing)

            parts = ing.split(' ')
            if len(parts) == 2:
                print ing

    connection.close()






# Run 
#analyse_problem()
#analyze_ingredients();
createNewCollection();