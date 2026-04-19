import pytest
from models import VehicleType, Vehicle, Auction
from parser import CarAuctionParser
from datetime import datetime

import warnings
from dateutil.parser import UnknownTimezoneWarning

warnings.filterwarnings("ignore", category=UnknownTimezoneWarning)  # silencing the warnin about time zones


def test_vehicle_creation():
    """Test to check the correct creation of the Vehicle object and type validation."""
    v = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
        vehicle_type=VehicleType.AUTOMOBILE,
        vin="12345",
        odometer=15000.5,
        color="Red"
    )
    assert v.year == 2020
    assert isinstance(v.odometer, float)


def test_invalid_vehicle_data():
    """Test to see if pydantic will report an error with invalid data."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        # Invalid vehicle manufacture date
        Vehicle(year="nowy", make="X", model="Y", vehicle_type=VehicleType.SUV,
                vin="1", odometer=0, color="Blue")


def test_parse_row_successful():
    """Test parsing the correct CSV → Auction + Vehicle row."""
    parser = CarAuctionParser()
    sample_row = {
        'Year': '2017',
        'Make': 'ACURA',
        'Model': 'RDX',
        'Vehicle Type': 'SUVs',
        'Vin#': '5J8TB4H54HL000609',
        'Odometer': '132,713 mi',
        'Exterior Color': 'Gray',
        'Auction Date': 'Tue Dec 09, 2025 8:30am CST',
        'Branch Name': 'Providence',
        'Region': 'East',
        'Loss Type': 'Collision'
    }

    auction = parser.parse_row(sample_row)

    assert isinstance(auction, Auction)
    assert isinstance(auction.auction_date, datetime)
    assert auction.branch_name == 'Providence'
    assert auction.location_region == 'East'

    v = auction.vehicle
    assert v.year == 2017
    assert v.make == 'ACURA'
    assert v.model == 'RDX'
    assert v.vehicle_type == VehicleType.SUV
    assert v.vin == '5J8TB4H54HL000609'
    assert v.odometer == 132713.0
    assert v.color == 'Gray'


def test_parse_row_invalid_vehicle_type_falls_back_to_unknown():
    """Unknown Vehicle Type handling test – should be UNKNOWN."""
    parser = CarAuctionParser()
    sample_row = {
        'Year': '2020',
        'Make': 'TEST',
        'Model': 'TEST',
        'Vehicle Type': 'CośTotalnieNieistniejącego',
        'Vin#': '1',
        'Odometer': '0 mi',
        'Exterior Color': 'Red',
        'Auction Date': '2025-01-01',
        'Branch Name': 'Test',
        'Region': 'Test',
        'Loss Type': 'Other'
    }

    auction = parser.parse_row(sample_row)
    assert auction.vehicle.vehicle_type == VehicleType.UNKNOWN


@pytest.mark.parametrize("odometer_str, expected_float", [
    ("132,713 mi", 132713.0),
    ("0 mi", 0.0),
    ("", 0.0),
    ("15000", 15000.0),
    ("1,234,567 mi", 1234567.0),
])
def test_odometer_parsing_various_formats(odometer_str, expected_float):
    """Test different Odometer field formats (with commas, spaces, empty)."""
    parser = CarAuctionParser()
    sample_row = {
        'Year': '2020',
        'Make': 'Toyota',
        'Model': 'Corolla',
        'Vehicle Type': 'Automobiles',
        'Vin#': '12345',
        'Odometer': odometer_str,
        'Exterior Color': 'Blue',
        'Auction Date': '2025-01-01',
        'Branch Name': 'Test',
        'Region': 'Test',
        'Loss Type': 'Other'
    }

    auction = parser.parse_row(sample_row)
    assert auction.vehicle.odometer == expected_float
