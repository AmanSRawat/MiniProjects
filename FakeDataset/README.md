# FakeDataset

A Python project that generates fake weather data and stores it in a MySQL database.

## Overview

This project provides two scripts:
1. **dataset-generate.py** - Generates fake weather records using Faker
2. **db.py** - Imports the generated CSV data into a MySQL database

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generate Fake Data

```bash
python dataset-generate.py
```

Generates 1000 fake weather records and saves to `fake_weather_data.csv`.

### Import to Database

```bash
python db.py
```

Reads the CSV file and inserts records into the MySQL `weatherdata` database.

## Database Configuration

Update the connection settings in `db.py` (line 4-10):

```python
host = "localhost"
user = "root"
password = "your_password"
database = "weatherdata"
```

## Data Schema

**weather table:**
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key, auto-increment |
| city | VARCHAR(255) | City name |
| temperature | FLOAT | Temperature in Celsius |
| condition | VARCHAR(255) | Weather condition (Sunny/Cloudy/Rainy/Snowy/Windy) |
| description | TEXT | Weather description |
| timestamp | DATETIME | Record timestamp |

## Generated Data Fields

- **city** - Random city name
- **temperature** - Random value between -10 and 40°C
- **condition** - One of: Sunny, Cloudy, Rainy, Snowy, Windy
- **description** - Random sentence
- **timestamp** - Random date/time within current year

## Dependencies

- pandas
- faker
- sqlalchemy
- mysql-connector-python
