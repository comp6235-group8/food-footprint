import json as js
def bad_waterfootprint():
    with open("popular/dishes.json") as jsonfile:
        json_data = js.load(jsonfile)
        print (json_data)

bad_waterfootprint()
