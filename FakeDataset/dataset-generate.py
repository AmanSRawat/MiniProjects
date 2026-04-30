# "city"
# "temperature"
# "condition"
# "description"
# "timestamp"

from faker import Faker
import pandas as pd
import random

fake = Faker()

def generate_weather_data(num_records):
    data = []
    conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"]
    
    for _ in range(num_records):
        record = {
            "city": fake.city(),
            "temperature": round(random.uniform(-10, 40), 2),  
            "condition": random.choice(conditions),
            "description": fake.sentence(),
            "timestamp": fake.date_time_this_year()
        }
        data.append(record)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    weather_data = generate_weather_data(1000)
    weather_data.to_csv("fake_weather_data.csv", index=False)
    print("Fake weather data generated and saved to 'fake_weather_data.csv'")