import asyncio
import csv
import io
import aiofiles
from abc import ABC, abstractmethod
from datetime import datetime
from dateutil import parser as date_parser

from models import Auction, Vehicle, VehicleType, LossType

import warnings
from dateutil.parser import UnknownTimezoneWarning

warnings.filterwarnings("ignore", category=UnknownTimezoneWarning)  # silencing the warnin about time zones


class DataParser(ABC):
    @abstractmethod
    def parse_row(self, row: dict) -> Auction:
        pass


class CarAuctionParser(DataParser):
    def parse_row(self, row: dict) -> Auction:
        """Safely parse a CSV line with handling invalid/unknown values."""

        vt_str = row.get('Vehicle Type', 'Unknown').strip()
        try:
            vehicle_type = VehicleType(vt_str)
        except ValueError:
            vehicle_type = VehicleType.UNKNOWN

        loss_str = row.get('Loss Type', '').strip()
        try:
            loss_type = LossType(loss_str) if loss_str else LossType.UNKNOWN
        except ValueError:
            loss_type = LossType.UNKNOWN

        raw_date = row.get('Auction Date', '')
        try:
            auction_date = date_parser.parse(raw_date)
        except (ValueError, TypeError):
            auction_date = datetime.now()

        # Data mapping for csv files
        vehicle = Vehicle(
            year=int(row['Year']),
            make=row['Make'],
            model=row['Model'],
            vehicle_type=vehicle_type,
            vin=row['Vin#'],
            odometer=row.get('Odometer', '0'),
            color=row['Exterior Color'],
            loss_type=loss_type
        )
        return Auction(
            auction_date=auction_date,
            branch_name=row['Branch Name'],
            location_region=row['Region'],
            vehicle=vehicle
        )


class AsyncAuctionProcessor:
    def __init__(self, parser: DataParser):
        self.parser = parser

    async def process_file(self, file_path: str) -> list[Auction]:
        """Asynchronously load and parse a single CSV file."""
        results = []

        try:
            async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                content = await f.read()
                reader = csv.DictReader(io.StringIO(content))
                for row in reader:
                    # try-except in case of invalid lines (Wichita - A LOAD TECHNOLOGY)
                    try:
                        auction = self.parser.parse_row(row)
                        results.append(auction)
                    except Exception:
                        continue
            print(f"Przetworzono plik: {file_path} ({len(results)} rekordów)")
        except Exception as e:
            print(f"Błąd w {file_path}: {e}")
        return results

    async def run_batch_processing(self, file_paths: list[str]):
        """Starts processing multiple files at once"""
        tasks = [self.process_file(path) for path in file_paths]
        return await asyncio.gather(*tasks)
