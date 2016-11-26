from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.group
collection = db.new_recipes
country = []

n = 0
print(collection.find()[1])
for i in collection.find():
    v = 0
    if 'ingredients' in i:
        for j in i['ingredients']:
           for p in country:
                if p == j:
                    v = 1
        if v != 1:
            country.append(j)
    n = n + 1
print(country.__len__())

