import requests
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.group
collection = db.new_recipes
start=[];
timeout=10.0
for i in range(410,2000):
    start.append(i*1000+1)
print(start)

#insert data into mongodb
def insert_data(js):
        collection.insert(js)
        
#collect data
def function_collect(start):
    for i in start:
        r=requests.get('http://api.yummly.com/v1/api/recipes?_app_id=44f270fb&_app_key=c5810cbfb615798aca16bdc80dec7f3a&&maxResult=500&&start='+str(i), headers={'Accept-Encoding': ''},timeout=None)
        print(r.status_code);
        print (int(i) - 1) / 1000
        if r.status_code==408:
            print "sss"
            start1 = []
            for i in range((int(i) - 1) / 1000, 1565):
                start1.append(i * 1000 + 1)
            function_collect(start1)
        else:
            N=0
            recipes=[]
            if r.json():
                recipes=r.json()["matches"]
            insert_data(recipes)
function_collect(start)