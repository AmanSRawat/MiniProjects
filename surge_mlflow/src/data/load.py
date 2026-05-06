import pandas as pd
from sqlalchemy import create_engine
import os

def load_data(db_url=None, table_name="weather")->pd.DataFrame:
    """Loads weather data from the specified database and table."""
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD")
    db = os.getenv("DB_NAME", "weather_data")

    db_url = db_url or f"mysql+pymysql://{user}:{password}@{host}/{db}"
    engine = create_engine(db_url)
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        print(f"Successfully loaded {len(df)} rows from {table_name}.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None