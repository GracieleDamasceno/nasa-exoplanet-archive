from pydantic import BaseModel, Field
from bson import ObjectId


class Planet(BaseModel):
    pl_name: str = Field(alias="PlanetName")
    sy_snum: str = Field(alias="NumberOfStars")
    sy_pnum: str = Field(alias="NumberOfPlanets")
    disc_year: str = Field(alias="DiscoveryYear")
    discoverymethod: str = Field(alias="DiscoveryMethod")
    disc_facility: str = Field(alias="DiscoverFacility")
    pl_orbper: str = Field(alias="OrbitalPeriod")
    pl_rade: str = Field(alias="PlanetEarthRadius")
    pl_bmasse: str = Field(alias="PlanetEarthMass")



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
        "planet_earth_mass": planet["pl_bmasse"]
    }
