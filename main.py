import asyncio

from parser import CarAuctionParser, AsyncAuctionProcessor

# constant value with the folder path
FOLDER = "iaai/"


async def main():
    file_names = [
        "Sales_List_03042024 (12).csv",
        "Sales_List_03052025 (24).csv",
        "Sales_List_04032025 (11).csv",
        "Sales_List_07092024 (35).csv",
        "Sales_List_09032025 (17).csv",
        "Sales_List_09032025 (20).csv",
        "Sales_List_10082024 (20).csv",
        "Sales_List_10102025 (12).csv",
        "Sales_List_10102025 (16).csv",
        "Sales_List_10312025 (11).csv",
        "Sales_List_10312025 (4).csv",
        "Sales_List_12012025 (11).csv",
        "Sales_List_12012025 (22).csv",
        "Sales_List_12012025 (3).csv",
        "Sales_List_12092025 (16).csv",
        "Sales_List_12092025 (3).csv"
    ]

    # Dynamic path creation with FOLDER const variable
    files = [f"{FOLDER}{name}" for name in file_names]

    parser = CarAuctionParser()
    processor = AsyncAuctionProcessor(parser)

    all_auctions = await processor.run_batch_processing(files)

    # Example display of results
    for batch in all_auctions:
        for auction in batch[:3]:  # Just the first 3 for example
            print(f"Aukcja w {auction.branch_name}: {auction.vehicle.make} {auction.vehicle.model}")


if __name__ == "__main__":
    asyncio.run(main())
