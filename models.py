from enum import StrEnum, auto


class VehicleType(StrEnum):
    # Vehicles - basic types
    AUTOMOBILE = "Automobiles"
    SUV = "SUVs"
    VAN = "Vans"
    PICKUP = "Pick-up Trucks"
    CLASSIC = "Classics"
    TRAILERS = "Trailers"
    HEAVY_DUTY_TRUCKS = "Heavy Duty Trucks"
    RECREATIONAL = "Recreational/ Miscellaneous"
    MOTORCYCLES = "Motorcycles"
    BUSES = "Buses"

    # Vehicles - complex types (Fleet / Rental)
    AUTOMOBILES_FLEET = "Automobiles,Fleet Vehicles"
    SUVS_FLEET = "SUVs,Fleet Vehicles"
    VANS_FLEET = "Vans,Fleet Vehicles"
    TRAILERS_FLEET = "Trailers,Fleet Vehicles"
    HEAVY_DUTY_TRUCKS_FLEET = "Heavy Duty Trucks,Fleet Vehicles"
    SUVS_RENTAL = "SUVs,Rental Vehicles"
    RECREATIONAL_FLEET = "Recreational/ Miscellaneous,Fleet Vehicles"

    UNKNOWN = "Unknown"


class LossType(StrEnum):
    COLLISION = "Collision"
    HAIL = "Hail"
    OTHER = "Other"
    UNKNOWN = "UNKNOWN"


from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, field_validator
from datetime import datetime
from typing import Optional


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Vehicle:
    year: int
    make: str
    model: str
    vehicle_type: VehicleType
    vin: str
    odometer: float
    color: str
    loss_type: LossType = LossType.UNKNOWN

    @field_validator('odometer', mode='before')
    @classmethod
    def clean_odometer(cls, v):
        if isinstance(v, str):
            v = v.replace(' mi', '').replace(',', '').strip()
            return float(v) if v else 0.0
        return v


@dataclass
class Auction:
    auction_date: datetime
    branch_name: str
    location_region: str
    vehicle: Vehicle
