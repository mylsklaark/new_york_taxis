import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import gzip
import shutil

def main(params):    
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # Define the .gz file and the name for the decompressed .csv file
    gz_name = 'yellow_tripdata_2021-01.csv.gz'
    csv_name = 'yellow_tripdata_2021-01.csv'

    print("Current directory:", os.getcwd())
    
    # Download the .gz file
    print(f"Downloading the file from {url}...")
    os.system(f"wget {url} -O {gz_name}")

    # Check if the file exists after download
    if not os.path.exists(gz_name):
        print(f"Failed to download {gz_name}.")
        return
    else:
        print(f"File downloaded successfully as {gz_name}. Now extracting...")

    # Decompress the .gz file to a .csv file
    with gzip.open(gz_name, 'rb') as f_in:
        with open(csv_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"File successfully extracted to {csv_name}")

    # Create PostgreSQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read the CSV file in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # Process the first chunk
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Create table in PostgreSQL (only once)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Insert the first chunk into PostgreSQL
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Process the remaining chunks
    while True:
        t_start = time()
        
        try:
            df = next(df_iter)
        except StopIteration:
            print("No more chunks to process.")
            break
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        # Insert the next chunk into PostgreSQL
        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()
        print(f"Inserted another chunk..., took {t_end - t_start:.3f} seconds")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where results will be written to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    
    main(args)
