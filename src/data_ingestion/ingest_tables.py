import argparse
import os
import shutil
import gzip
from time import time
import pandas as pd
from sqlalchemy import create_engine

def process_file(url, table_name, engine):
    file_name = f"{table_name}.csv.gz"
    if url.endswith(".csv"):
        file_name = f"{table_name}.csv"

    print(f"Downloading file from {url}...")
    os.system(f"wget {url} -O {file_name}")

    if not os.path.exists(file_name):
        print(f"Failed to download {file_name}.")
        return
    else:
        print(f"File downloaded successfully as {file_name}. Now extracting..." if file_name.endswith(".gz") else "File is not compressed, proceeding to process...")

    if file_name.endswith(".gz"):
        csv_name = f"{table_name}.csv"
        with gzip.open(file_name, "rb") as f_in:
            with open(csv_name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"File successfully extracted to {csv_name}")
    else:
        csv_name = file_name

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    else:
        print("Column 'tpep_pickup_datetime' not found. Skipping datetime conversion for this column.")

    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    else:
        print("Column 'tpep_dropoff_datetime' not found. Skipping datetime conversion for this column.")

    print(f"Inserting data into {table_name}")
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")

    while True:
        t_start = time()

        try:
            df = next(df_iter)
        except StopIteration:
            print("No more chunks to process.")
            break

        if 'tpep_pickup_datetime' in df.columns:
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        else:
            print("Column 'tpep_pickup_datetime' not found in chunk. Skipping datetime conversion for this column.")

        if 'tpep_dropoff_datetime' in df.columns:
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        else:
            print("Column 'tpep_dropoff_datetime' not found in chunk. Skipping datetime conversion for this column.")

        df.to_sql(name=table_name, con=engine, if_exists="append")
        print(f"Inserted chunk into {table_name}")

        t_end = time()
        print(f"Inserted another chunk..., took {t_end - t_start:.3f} seconds")

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    urls_and_tables = [
        (params.url, params.table_name_1),
        (params.url_2, params.table_name_2)
    ]

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    for url, table_name in urls_and_tables:
        process_file(url, table_name, engine)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name for postgres")
    parser.add_argument(
        "--table_name_1", help="name of the table for the first CSV file"
    )
    parser.add_argument(
        "--table_name_2", help="name of the table for the second CSV file"
    )
    parser.add_argument("--url", help="url of the first csv file")
    parser.add_argument("--url_2", help="url of the second csv file")

    args = parser.parse_args()

    main(args)