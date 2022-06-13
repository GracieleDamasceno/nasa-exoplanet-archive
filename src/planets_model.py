from pydantic import BaseModel, Field
from bson import ObjectId


class Planet(BaseModel):
    pl_name: str = Field(alias="planet_name")
    sy_snum: str = Field(alias="number_of_stars")
    sy_pnum: str = Field(alias="number_of_planets")
    disc_year: str = Field(alias="discovery_year")
    discoverymethod: str = Field(alias="discovery_method")
    disc_facility: str = Field(alias="discovery_facility")
    pl_orbper: str = Field(alias="orbital_period")
    pl_rade: str = Field(alias="planet_earth_radius")
    pl_bmasse: str = Field(alias="planet_earth_mass")
    link: str


def planet_helper(planet) -> dict:
    return {
        "id": str(planet["_id"]),
        "planet_name": planet["pl_name"],
        "number_of_stars": planet["sy_snum"],
        "number_of_planets": planet["sy_pnum"],
        "discovery_year": planet["disc_year"],
        "discovery_method": planet["discoverymethod"],
        "discovery_facility": planet["disc_facility"],
        "orbital_period": planet["pl_orbper"],
        "planet_earth_radius": planet["pl_rade"],
        "planet_earth_mass": planet["pl_bmasse"],
        "link": planet["link"]
    }


def ResponseModel(data, code, message):
    return {
        "code": code,
        "message": message,
        "data": data,
    }
