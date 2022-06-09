from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client["nasa-exoplanet-archive"]
planets_collection = db["planets"]
