import pandas as pd
from sqlalchemy import create_engine
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(db_url)

def upload_data_to_db(df, table_name, if_exists='replace'):
    """
    Uploads a DataFrame to the database and ensures the connection is closed properly.
    This prevents database locking issues (deadlocks).
    """
    engine = get_engine()
    try:
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, chunksize=1000)
        print(f"Success: Data uploaded to table '{table_name}'.")
    except Exception as e:
        print(f"An error occurred during the upload process: {e}")
    finally:
        engine.dispose()
        print("Database connection closed successfully.")

def run_raw_upload():
    """
    Main function to clean the raw CSV data and push it to the database.
    """
    csv_path = "data/raw/AmesHousing.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find the file at {csv_path}. Please check the path.")
        return

    df = pd.read_csv(csv_path)
    df.columns = [re.sub(r'[/ ]', '_', c.lower()) for c in df.columns]
    
    upload_data_to_db(df, 'raw_housing_data')

if __name__ == "__main__":
    run_raw_upload()