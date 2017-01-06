import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

#####################################################33
### Data crawling
response = urllib2.urlopen("https://www.cia.gov/library/publications/the-world-factbook/fields/2201.html")
page_source = response.read()
# print page_source
soup = BeautifulSoup(page_source, "html.parser")
table = soup.find("table", attrs={"id":"fieldListing"})

# The first tr contains the field names.
headings = [th.get_text() for th in table.find("tr").find_all("th")]
#print "Headings: " 
#print headings

dataset0 = []
for table_row in table.find_all("tr")[1:]:
    cells = [td.get_text().replace('\n', '') for td in table_row.find_all("td")]
    dataset0.append(cells);

#print "Datasets:"
#print dataset0



#####################################################33
### Data extraction
dataset = []
for row in dataset0:
    # print row
    # Parse each entry
    entry = {}
    # Extract country
    entry['country'] = row[0]
    # Extract value
    parts = row[1].split(' ')  # Split the second field to extract the value
    if len(parts[0].upper()) > 0 and parts[0].upper() != 'NA':
        entry['value'] = float(parts[0].replace(',', ''))
    else:
        entry['value'] = None
    # Extract year
    m = re.search('\((\d{2,4})\)', row[1])
    if m:
        year_str = m.group(1)
        year = int(year_str)
        entry['year'] = year
    else:
        entry['year'] = None
    # print entry
    dataset.append(entry)
    # break

#for i in range(1, 100):
#    print i, dataset[i]



#####################################################33
### Store to MongoDB
client = MongoClient()
#db = client.waterfp
db = client["water_footprint"]
collection = db.tot_renew_water
collection.insert(dataset)
