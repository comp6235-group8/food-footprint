from pymongo import MongoClient
import requests
import json
import numpy
client = MongoClient('mongodb://localhost:27017')
db = client.group
collection1 = db.new_recipes
collection2 = db.ingredients
ingredient = []
import sys;
reload(sys);
sys.setdefaultencoding("utf8")
def fun_ingredient():
    for i in collection1.find():
        v = 0
        if 'ingredients' in i:
            for j in i['ingredients']:
                for p in ingredient:
                    if p == j:
                        v = 1
                if v != 1:
                    ingredient.append(j)
                n = n + 1
    collection2.insert({"ingredient":ingredient})
def show_data():
    for i in collection2.find():
        print i
def fun_translate():
    result=[""];
    for i in collection2.find():
        for j in i['ingredient']:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q="+j;
            header = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'Keep-Alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            r=requests.get(url, headers=header).text
            array=r.split(',')
            result.append(array[0][4:-1])
    print result
    return result

def savetxt(filename,x):
    numpy.savetxt(filename,x,fmt='%s',newline='\n')

result=fun_translate()
savetxt("ingredient",result)