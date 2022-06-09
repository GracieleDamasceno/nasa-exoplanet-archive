from pydantic import BaseModel, Field
from bson import ObjectId


class Planet(BaseModel):
    pl_name: str = Field(None, alias="PlanetName")
    sy_snum: str = Field(None, alias="NumberOfStars")
    sy_pnum: str = Field(None, alias="NumberOfPlanets")
    disc_year: str = Field(None, alias="DiscoveryYear")
    discoverymethod: str = Field(None, alias="DiscoveryMethod")
    disc_facility: str = Field(None, alias="DiscoverFacility")
    pl_orbper: str = Field(None, alias="OrbitalPeriod")
    pl_rade: str = Field(None, alias="PlanetEarthRadius")
    pl_bmasse: str = Field(None, alias="PlanetEarthMass")
