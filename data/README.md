# Mongodb 

Database name: water_foodprint

## Create collections
* `mongoimport -d water_footprint -c animal_products --file animal_products.json`
* `mongoimport -d water_footprint -c crop_products --file crop_products.json`
* `mongoimport -d water_footprint -c crop_products_aggregated_by_category --file crop_products_aggregated_by_category.json`
* `mongoimport -d water_footprint -c crop_products_by_category --file crop_products_by_category.json`
* `mongoimport -d water_footprint -c ingredient_to_waterfootprint --file ingredient_to_waterfootprint.json`
* `mongoimport -d water_footprint -c recipes_2 --file recipes_2_water.json`
