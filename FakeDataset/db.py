import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def create_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "weather_data")
    )

data = pd.read_csv("fake_weather_data.csv")

data_to_insert = data[['city', 'temperature', 'condition', 'description', 'timestamp','surge']].values.tolist()

connection = create_connection()
conn = connection.cursor()

conn.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        city VARCHAR(255), 
        temperature FLOAT, 
        `condition` VARCHAR(255), 
        description TEXT, 
        timestamp DATETIME,
        surge FLOAT
    )
""")


sql = "INSERT INTO weather (city, temperature, `condition`, description, timestamp,surge) VALUES (%s, %s, %s, %s, %s,%s)"

conn.executemany(sql, data_to_insert)

connection.commit()
print(f"Successfully inserted {conn.rowcount} rows.")

conn.close()
connection.close()