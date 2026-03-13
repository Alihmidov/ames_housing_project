import pandas as pd
from sqlalchemy import create_engine
import os
import re
from dotenv import load_dotenv

load_dotenv() # reads .env file

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def upload_raw_data():
    csv_path = "data/raw/AmesHousing.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        print("Please download the AmesHousing.csv and place it in the 'data/raw/' folder.")
        return

    try:
        engine = create_engine(DATABASE_URL)
        df = pd.read_csv(csv_path)
        
        df.columns = [re.sub(r'[/ ]', '_', c.lower()) for c in df.columns]
        
        df.to_sql('raw_housing_data', engine, if_exists='replace', index=False, chunksize=500)
        
        print("Success: Data has been uploaded to the PostgreSQL database.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    upload_raw_data()