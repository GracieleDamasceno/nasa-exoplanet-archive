import sys

from fastapi import FastAPI
from pymongo import MongoClient
from planets_model import *

sys.path.append("server")
client = MongoClient("localhost", 27017)
db = client["nasa-exoplanet-archive"]
planets_collection = db["planets"]
app = FastAPI()


@app.get("/", tags=["main"])
async def main():
    return {"message": "Nasa Exoplanet Archive is on!"}


@app.get("/planets", tags=["planets"])
async def main():
    """Get all planets paginated without filters"""
    planets = []
    for planet in planets_collection.find({}).limit(10):
        planets.append(planet_helper(planet))
    return planets
