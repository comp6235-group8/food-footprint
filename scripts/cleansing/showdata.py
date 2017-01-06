# -*- coding: utf-8 -*-
from pymongo import MongoClient
import requests
import re
import json
import numpy


client = MongoClient('mongodb://localhost:27017')
db = client.water_footprint
collection1 = db.water_footprint
collection2 = db.recipes
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


    #clean data
def fun_translate(collection,part):
    result=[""];
    print collection;
    for i in collection.find().limit(300):
            i[part] = re.sub(r"&", "@12", i[part])
            num = re.sub(r'\{.*?\}', "", i[part])
            num = re.sub(r'\(.*?\)', "", num)
            num = re.sub(r'\<g.*?g\>', "", num)
            num = re.sub(r'\\m/.*?\\m/', "", num)
            num = re.sub(r'</br>', "", num)
            num = re.sub(r'//', "", num)
            num = re.sub(r'\<span\>.*?\<\/span\>', "", num)
            num = re.sub(r'\<em\>.*?\<\/em\>', "", num)
            # for j in i[part]:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q="+num;
            header = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'Keep-Alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            r=requests.get(url,headers=header).text
            array=r.split('",');
            num=array[0][4:]
            num = re.sub(r"@12", "&", num)
            num = re.sub(r"’", "'", num)
            print num
            num = re.sub(r'[^a-zA-Z   ‎&0-9\/’\'\‘\’\"\"\“\”,΄.&Øøłướịççảáåỏốôòōöởíıïäàóšñéèëâêêñńûúùüůšæ%ğÁÉ++£«»è ×—–-]', "",num)
            print num
            result.append(num)
    print result
    return result

def savetxt(filename,x):
    numpy.savetxt(filename,x,fmt='%s',newline='\n')

result=fun_translate(collection2,"recipeName")
savetxt("ingredient",result)

