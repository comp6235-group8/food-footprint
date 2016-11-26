import requests
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.group
collection = db.new_recipes
start=[];
for i in range(16,1565):
    start.append(i*1000)
print(start)

#insert data into mongodb
def insert_data(js):
    for recipe in js:
        p=0
        for i in collection.find():
            if i["id"]==recipe['id']:
                p=1;
            else:
                pass
        if(p==0):
            collection.insert_one(recipe)
        else:
            print (recipe['recipeName'],"has been inserted")

#collect data
for i in start:
    r=requests.get('http://api.yummly.com/v1/api/recipes?_app_id=44f270fb&_app_key=c5810cbfb615798aca16bdc80dec7f3a&&maxResult=1000&&start='+str(i), headers={'Accept-Encoding': ''})
    N=0
    recipes=[]
    if "matches" in r.json():
        recipes=r.json()["matches"]
    insert_data(recipes)
