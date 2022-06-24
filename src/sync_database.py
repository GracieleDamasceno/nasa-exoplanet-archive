import requests
from pymongo import MongoClient
from database import *

file_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,sy_snum,sy_pnum,disc_year," \
           "discoverymethod,disc_facility,disc_locale,disc_telescope,pl_orbper,pl_rade,pl_bmasse+from+ps&format=json"


def sync_database():
    try:
        response = requests.get(file_url)
        data = response.json()
        for i in range(len(data)):
            data[i].update({"link": "https://exoplanetarchive.ipac.caltech.edu/overview/"+str(data[i]["pl_name"])})
        planets_collection.delete_many({})
        inserted = planets_collection.insert_many(data)
        return True, "Database successfully updated "+str(len(inserted.inserted_ids))+" elements", len(inserted.inserted_ids)
    except Exception as exception:
        return False, "An error occurred when updating database: "+str(exception)
