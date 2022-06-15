from fastapi import FastAPI
from planets_model import *
from sync_database import *
from database import *
from typing import Union
import re

app = FastAPI()


@app.get("/sync-database", tags=["settings"])
async def sync_local_database_with_exoplanet_archive_database():
    """Sync local database with exo-planet archive database"""
    success, message = sync_database()
    if success:
        return ResponseModel("", 200, message, 1)
    else:
        return ResponseModel("", 500, message, 1)


@app.get("/planets", tags=["planets"])
async def get_planets_paginated_with_filters(size: int = 10, page_num: int = 1,
                                             planet_name: Union[str, None] = None,
                                             discovery_method: Union[str, None] = None,
                                             discovery_facility: Union[str, None] = None,
                                             discovery_year: Union[str, None] = None):
    """Get all planets paginated with filters"""
    query_filter = []
    if planet_name is not None:
        query_filter.append({"pl_name": {"$regex": re.compile(planet_name, re.IGNORECASE)}})
    if discovery_method is not None:
        query_filter.append({"discoverymethod": re.compile(discovery_method, re.IGNORECASE)})
    if discovery_facility is not None:
        query_filter.append({"disc_facility": re.compile(discovery_facility, re.IGNORECASE)})
    if discovery_year is not None:
        query_filter.append({"disc_year": int(discovery_year)})

    condition = {"$and": query_filter}
    planets = []
    skips = size * (page_num - 1)
    count = planets_collection.estimated_document_count({})
    for planet in planets_collection.find(condition).skip(skips).limit(size).sort("disc_year", -1):
        planets.append(planet_helper(planet))
    return ResponseModel(planets, 200, "Planets successfully retrieved", count)
