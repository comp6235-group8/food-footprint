# What Dishes and their Ingredients Have the Highest Water Footprint?

## Requirements
1. Make sure you have python 2.7 installed
2. `pip install -r requirements.txt`
3. Make sure you have a local MongoDB installed
4. Import collections manually/run python scripts to load collections into MongoDB.
   To import the collections manually:
    * Download the files (through the browser) from https://mega.nz/#!8lFSEJzQ!O_VO7tkOZSf_LZPI6tEsxZ3LhqvrseNjAyH0-gR130U
    * Start the local mongodb on default port: `mongod`
    * Create collections (given that the files are in the same directory)
    * `mongoimport -d water_footprint -c animal_products --file animal_products.json`
    * `mongoimport -d water_footprint -c crop_products --file crop_products.json`
    * `mongoimport -d water_footprint -c crop_products_aggregated_by_category --file crop_products_aggregated_by_category.json`
    * `mongoimport -d water_footprint -c crop_products_by_category --file crop_products_by_category.json`
    * `mongoimport -d water_footprint -c ingredient_to_waterfootprint --file ingredient_to_waterfootprint.json`
    * `mongoimport -d water_footprint -c recipes_2 --file recipes_2_water.json`

## To get the backend application running
1. Make sure you have a local mongodb instance running: `mongod`
2. `cd` into `gui-prototype`
3. Run `python app.py`
4. Navigate to localhost:5000 in your favourite browser
