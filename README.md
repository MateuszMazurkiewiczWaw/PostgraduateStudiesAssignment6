# Car Auction Data Processor

Final project for the **Advanced Python Programming** course at **SGGW (Warsaw University of Life Sciences)**.

The application is designed for the asynchronous processing and validation of CSV data regarding automobile auctions in the USA.

##  Key Features & Criteria Met

This project was implemented with a focus on code quality, clean architecture, and modern Python practices:

-   **Data Storage (`dataclasses`):** Utilizes `pydantic.dataclasses` to structure data for both auctions and vehicles.
    
-   **Asynchronous Processing (`asyncio` + `aiofiles`):** Implements parallel reading and parsing of multiple CSV files without blocking the event loop.
    
-   **SOLID Principles & Design Patterns:**
    
    -   **Strategy Pattern:** The `CarAuctionParser` class implements the `DataParser` interface, allowing for easy transitions between different input formats.
        
    -   **Dependency Inversion Principle (DIP):** The processor depends on the parser abstraction rather than a specific implementation.
        
-   **Data Validation:** Uses Pydantic's `@field_validator` for automatic data cleaning (e.g., removing "mi" units and commas from odometer strings).
    
-   **Type Hinting:** Comprehensive and strict type annotations used throughout the entire project.
    
-   **Enums:** Employs `StrEnum` to categorize vehicle types and loss types effectively.
    
-   **Unit Testing:** A suite of `pytest` tests covering critical parsing and validation logic.
    

##  Installation & Requirements

The project requires **Python 3.11+**.

1.  Install the required libraries:
    
    Bash
    
    ```
    pip install pydantic python-dateutil aiofiles pytest
    
    ```
    
2.  Place the source `.csv` files in the directory specified by the `FOLDER` constant in `main.py` (default is `iaai/`).
    

##  Usage

To run the main data processing script:

Bash

```
python main.py

```

To run the unit tests:

Bash

```
pytest test_auction.py -v

```

##  Architecture

The project consists of the following modules:

-   `models.py` – Data model definitions and Pydantic validators.
    
-   `parser.py` – CSV parsing logic and the asynchronous processing engine.
    
-   `main.py` – The application entry point.
    
-   `test_auction.py` – Unit tests for critical components.
    
-   `UML_Diagram.png` – Class structure visualization (generated via PlantUML).
