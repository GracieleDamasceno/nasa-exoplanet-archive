import sys
from typing import List

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


@app.get("/planets", tags=["planets"], response_model=Planet)
async def main():
    """Get all planets without filters"""
    response = []
    for element in planets_collection.find({}).limit(1):
        response.append(element)
    return response[0]
