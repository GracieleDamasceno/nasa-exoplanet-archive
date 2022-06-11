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
async def get_planets_paginated_without_filters(size: int = 10, page_num: int = 1):
    """Get all planets paginated without filters"""
    planets = []
    skips = size * (page_num - 1)
    for planet in planets_collection.find({}).skip(skips).limit(size):
        planets.append(planet_helper(planet))
    return ResponseModel(planets, 200, "Planets successfully retrieved")
