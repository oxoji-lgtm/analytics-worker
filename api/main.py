import logging
import os
import sys
from datetime import datetime
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not set.")
    sys.exit(1)

def fetch_data(query: str) -> Optional[pd.DataFrame]:
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)
            logger.info(f"Fetched {len(df)} records.")
            return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['processed_at'] = datetime.now()
        df['processed_flag'] = True
        logger.info("Data processed successfully.")
        return df
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise

def save_data(df: pd.DataFrame, table_name: str) -> None:
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            df.to_sql(table_name, connection, if_exists='append', index=False)
            logger.info(f"Data saved to {table_name}.")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise

def main():
    query = "SELECT * FROM raw_data WHERE processed_flag = False;"
    table_name = "processed_data"

    df = fetch_data(query)
    if df is not None and not df.empty:
        processed_df = process_data(df)
        save_data(processed_df, table_name)

if __name__ == "__main__":
    main()