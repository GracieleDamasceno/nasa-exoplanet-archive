import requests
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["nasa-exoplanet-archive"]
collection = db["planets"]
file_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,sy_snum,sy_pnum,disc_year,discoverymethod,disc_facility,pl_orbper,pl_rade,pl_bmasse+from+ps&format=json"

response = requests.get(file_url)
data = response.json()
collection.insert_many(data)
