from pymongo import MongoClient
import numpy

client = MongoClient()
db = client["water_footprint"]
collection = db["crop_products_by_category"]

current_category = collection.find_one()["product_category"]
aggregated_result = []

default_category_acc = {
    "product": current_category, "global_wf": {"blue": 0, "green": 0, "grey": 0},
    "wf_acc": {"blue": [], "green": [], "grey": []},
    "country_acc": {},
    "countries": []
}

current_category_acc = {
    "product": current_category, "global_wf": {"blue": 0, "green": 0, "grey": 0},
    "wf_acc": {"blue": [], "green": [], "grey": []},
    "country_acc": {},
    "countries": []
}

for doc in collection.find():
    if doc["product_category"] == current_category:
        print doc["water_footprint_global_average"]["blue"], doc["water_footprint_global_average"]["green"], doc["water_footprint_global_average"]["grey"]
        if doc["water_footprint_global_average"]["blue"]:
            current_category_acc["wf_acc"]["blue"].append(doc["water_footprint_global_average"]["blue"])
        if doc["water_footprint_global_average"]["green"]:
            current_category_acc["wf_acc"]["green"].append(doc["water_footprint_global_average"]["green"])
        if doc["water_footprint_global_average"]["grey"]:
            current_category_acc["wf_acc"]["grey"].append(doc["water_footprint_global_average"]["grey"])

        for country in doc["countries"]:
            country_name = country["country"]
            if country_name not in current_category_acc["country_acc"]:
                current_category_acc["country_acc"][country_name] = {"blue": [], "green": [], "grey": []}
            else:
                if country["water_footprint_country_average"]["blue"]:
                    current_category_acc["country_acc"][country_name]["blue"].append(
                        country["water_footprint_country_average"]["blue"]
                    )
                if country["water_footprint_country_average"]["green"]:
                    current_category_acc["country_acc"][country_name]["green"].append(
                        country["water_footprint_country_average"]["green"]
                    )
                if country["water_footprint_country_average"]["grey"]:
                    current_category_acc["country_acc"][country_name]["grey"].append(
                        country["water_footprint_country_average"]["grey"]
                    )
    else:
        if current_category_acc["wf_acc"]["blue"]:
            current_category_acc["global_wf"]["blue"] = numpy.mean(current_category_acc["wf_acc"]["blue"])
        else:
            current_category_acc["global_wf"]["blue"] = None
        if current_category_acc["wf_acc"]["green"]:
            current_category_acc["global_wf"]["green"] = numpy.mean(current_category_acc["wf_acc"]["green"])
        else:
            current_category_acc["global_wf"]["green"] = None
        if current_category_acc["wf_acc"]["grey"]:
            current_category_acc["global_wf"]["grey"] = numpy.mean(current_category_acc["wf_acc"]["grey"])
        else:
            current_category_acc["global_wf"]["grey"] = None

        print "avg"
        print current_category_acc["global_wf"]["blue"], current_category_acc["global_wf"]["green"], current_category_acc["global_wf"]["grey"]
        print doc["product_category"]
        print "values"

        for country, wf in current_category_acc["country_acc"].iteritems():
            wf_types = {"blue": None, "green": None, "grey": None}
            for fp_type in ["blue", "green", "grey"]:
                if wf[fp_type]:
                    wf_types[fp_type] = numpy.mean(wf[fp_type])

            current_category_acc["countries"].append({
                "country": country,
                "wf_country_average": {
                    "blue": wf_types["blue"],
                    "green": wf_types["green"],
                    "grey": wf_types["grey"]
                }
            })
        aggregated_result.append(current_category_acc)
        # aggregated_result.append({
        #     "product": current_category_acc["product"],
        #     "global_wf": current_category_acc["global_wf"],
        #     "countries": current_category_acc["countries"]
        # })

        current_category = doc["product_category"]
        current_category_acc = {
            "product": current_category, "global_wf": {"blue": 0, "green": 0, "grey": 0},
            "wf_acc": {"blue": [], "green": [], "grey": []},
            "country_acc": {},
            "countries": []
        }

        print doc["water_footprint_global_average"]["blue"], doc["water_footprint_global_average"]["green"], doc["water_footprint_global_average"]["grey"]

        if doc["water_footprint_global_average"]["blue"]:
            current_category_acc["wf_acc"]["blue"].append(doc["water_footprint_global_average"]["blue"])
        if doc["water_footprint_global_average"]["green"]:
            current_category_acc["wf_acc"]["green"].append(doc["water_footprint_global_average"]["green"])
        if doc["water_footprint_global_average"]["green"]:
            current_category_acc["wf_acc"]["grey"].append(doc["water_footprint_global_average"]["grey"])

        # This should be extracted into a function
        for country in doc["countries"]:
            country_name = country["country"]
            if country_name not in current_category_acc["country_acc"]:
                current_category_acc["country_acc"][country_name] = {"blue": [], "green": [], "grey": []}
            else:
                if country["water_footprint_country_average"]["blue"]:
                    current_category_acc["country_acc"][country_name]["blue"].append(
                        country["water_footprint_country_average"]["blue"]
                    )
                if country["water_footprint_country_average"]["green"]:
                    current_category_acc["country_acc"][country_name]["green"].append(
                        country["water_footprint_country_average"]["green"]
                    )
                if country["water_footprint_country_average"]["grey"]:
                    current_category_acc["country_acc"][country_name]["grey"].append(
                        country["water_footprint_country_average"]["grey"]
                    )

print len(aggregated_result)
print aggregated_result[0]["product"], aggregated_result[0]["global_wf"]
