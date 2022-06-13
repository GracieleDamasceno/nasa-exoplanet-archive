from fastapi import FastAPI
from planets_model import *
from sync_database import *
from database import *
app = FastAPI()


@app.get("/sync-database", tags=["settings"])
async def sync_local_database_with_exoplanet_archive_database():
    """Sync local database with exo-planet archive database"""
    success, message = sync_database()
    if success:
        return ResponseModel("", 200, message)
    else:
        return ResponseModel("", 500, message)


@app.get("/planets", tags=["planets"])
async def get_planets_paginated_without_filters(size: int = 10, page_num: int = 1):
    """Get all planets paginated without filters"""
    planets = []
    skips = size * (page_num - 1)
    for planet in planets_collection.find({}).skip(skips).limit(size).sort("disc_year", -1):
        planets.append(planet_helper(planet))
    return ResponseModel(planets, 200, "Planets successfully retrieved")
