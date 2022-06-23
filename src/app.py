import pymongo
from fastapi import FastAPI
from planets_model import *
from sync_database import *
from database import *
from typing import Union
from fastapi.responses import FileResponse
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import matplotlib.pyplot as plt
import re

app = FastAPI()


@app.get("/sync-database", tags=["settings"])
async def sync_local_database_with_exoplanet_archive_database():
    """Sync local database with exo-planet archive database"""
    success, message = sync_database()
    if success:
        return ResponseModel("", 200, message, 0)
    else:
        return ResponseModel("", 500, message, 0)


@app.get("/planets", tags=["planets"])
async def get_planets_paginated_with_filters(planet_name: Union[str, None] = None,
                                             discovery_method: Union[str, None] = None,
                                             discovery_facility: Union[str, None] = None,
                                             discovery_year: Union[str, None] = None,
                                             size: int = 10, page_num: int = 1, ordered: str = "desc"):
    """Get all planets paginated with filters"""
    try:
        query_filter = []
        if planet_name is not None:
            query_filter.append({"pl_name": {"$regex": re.compile(planet_name, re.IGNORECASE)}})
        if discovery_method is not None:
            query_filter.append({"discoverymethod": re.compile(discovery_method, re.IGNORECASE)})
        if discovery_facility is not None:
            query_filter.append({"disc_facility": re.compile(discovery_facility, re.IGNORECASE)})
        if discovery_year is not None:
            query_filter.append({"disc_year": int(discovery_year)})

        if query_filter:
            condition = {"$and": query_filter}
        else:
            condition = {}

        if ordered == "desc":
            ordered = -1
        elif ordered == "asc":
            ordered = 1
        else:
            return ResponseModel("", 500,
                                 "An error occurred while fetching data: key order must be asc (for ascending) or desc (for descending)",
                                 0)

        planets = []
        skips = size * (page_num - 1)
        count = len(list(planets_collection.find(condition)))
        for planet in planets_collection.find(condition).skip(skips).limit(size).sort("disc_year", ordered):
            planets.append(planet_helper(planet))
        return ResponseModel(planets, 200, "Planets successfully retrieved", count)
    except Exception as exception:
        return ResponseModel("", 500, "An error occurred while fetching data: " + str(exception), 1)


@app.get("/plot/planet/discovery-year", tags=["planets"])
async def get_number_of_planets_discovered_by_year_plotted_in_graph():
    """Get number of discovered planets by year plotted in a graph"""
    group_by_year = {
        "$group": {
            "_id": "$disc_year",
            "planets_discovered": {"$sum": 1}
        }
    }

    sort_by_year = {
        "$sort": {"_id": pymongo.ASCENDING}
    }

    mongo_data = list(planets_collection.aggregate([group_by_year, sort_by_year]))

    data = pd.DataFrame(mongo_data)
    data.sort_values(by='_id', ascending=True)
    data.plot(kind='bar', x='_id', y='planets_discovered')
    plt.yscale('log')
    plt.xlabel('Discovery Year')
    plt.ylabel('Planets Discovered')
    plt.title("Number of planets discovered by year")
    ax = plt.gca()
    for axis in [ax.yaxis]:
        formatter = ScalarFormatter()
        formatter.set_scientific(False)
        axis.set_major_formatter(formatter)
    plt.savefig('planets_by_year.png', bbox_inches="tight", dpi=200)
    return FileResponse('planets_by_year.png')


@app.get("/plot/planet/discovery-method", tags=["planets"])
async def get_number_of_planets_discovered_by_discovery_method_plotted_in_graph():
    """Get number of discovered planets by year plotted in a graph"""
    group_by_year = {
        "$group": {
            "_id": "$discoverymethod",
            "planets_discovered": {"$sum": 1}
        }
    }

    mongo_data = list(planets_collection.aggregate([group_by_year]))

    data = pd.DataFrame(mongo_data)
    data.sort_values(by='_id', ascending=True)
    data.plot.barh(x='_id', y='planets_discovered')
    plt.xscale('log')
    plt.xlabel('Discovery Method')
    plt.ylabel('Planets Discovered')
    plt.title("Number of planets discovered by discovery method")
    ax = plt.gca()
    for axis in [ax.xaxis]:
        formatter = ScalarFormatter()
        formatter.set_scientific(False)
        axis.set_major_formatter(formatter)
    plt.savefig('planets_by_year.png', bbox_inches="tight", dpi=200)
    return FileResponse('planets_by_year.png')


@app.get("/plot/planet/discovery-facility", tags=["planets"])
async def get_number_of_planets_discovered_by_discovery_facility_plotted_in_graph():
    """Get number of discovered planets by year plotted in a graph"""
    group_by_year = {
        "$group": {
            "_id": "$disc_facility",
            "planets_discovered": {"$sum": 1}
        }
    }
    sort_by_facility = {
        "$sort": {"planets_discovered": pymongo.ASCENDING}
    }

    mongo_data = list(planets_collection.aggregate([group_by_year, sort_by_facility]))

    data = pd.DataFrame(mongo_data)
    data.sort_values(by='_id', ascending=True)
    data.plot.barh(x='_id', y='planets_discovered', fontsize=6)
    plt.xscale('log')
    plt.ylabel('Discovery Facility', fontsize=6)
    plt.xlabel('Planets Discovered', fontsize=6)
    plt.title("Number of planets discovered by discovery facility", fontsize=6)
    ax = plt.gca()

    for axis in [ax.xaxis]:
        formatter = ScalarFormatter()
        formatter.set_scientific(False)
        axis.set_major_formatter(formatter)

    plt.tick_params(axis='y', which='major', labelsize=4)
    plt.savefig('planets_by_year.png', bbox_inches="tight", dpi=400)
    return FileResponse('planets_by_year.png')
