import pandas as pd
from sqlalchemy import create_engine
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_data(db_url=None, table_name="weather") -> pd.DataFrame:
    """Loads weather data from the specified database and table."""
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "") 
    db = os.getenv("DB_NAME", "weatherdata")

    # 2. URL-encode the password to handle special characters
    safe_password = urllib.parse.quote_plus(password)

    if not db_url:
        db_url = f"mysql+pymysql://{user}:{safe_password}@{host}/{db}"
    
    # 3. Add pool_pre_ping to handle stale connections gracefully
    engine = create_engine(db_url, pool_pre_ping=True)
    
    try:
        # 4. Use a context manager to ensure the connection is closed
        with engine.connect() as connection:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, connection)
            print(f"Successfully loaded {len(df)} rows from {table_name}.")
            return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None