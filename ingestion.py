# ingestion.py: load NY taxi data into a postgres container
import pandas as pd
import sqlalchemy
import os

# Columns to convert to datetime
parse_dates = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

# The following file was downloaded with a RUN instruction
# in the "Dockerfile-ingestion" file
green_df = pd.read_csv("green_2019.csv.gz",
                       compression="gzip",
                       iterator=True,
                       chunksize=100_000, # Read file in chunks of 100_000
                       parse_dates=parse_dates)

# This is a small file
zones_df = pd.read_csv("zones.csv")

# Create engine to establish a connection with the Postgres database
engine = sqlalchemy.create_engine(f"postgresql://"
                                  f"{os.environ['POSTGRES_USER']}:"
                                  f"{os.environ['POSTGRES_PASSWORD']}@"
                                  "postgres_container:5432/"
                                  f"{os.environ['POSTGRES_DB']}")


# Establish the connection to start inserting data
with engine.connect() as connection:
    i, total_rows = 0, 0
    print("-" * 20)

    # Write chunks to Postgres
    for chunk in green_df:
        print(f"Iteration {i}:\n")
        print(f"Writing {chunk.shape[0]} rows to table: green_taxi_2019 ...")

        chunk.to_sql("green_taxi_2019", con=connection, if_exists="append")
        connection.commit()

        print("-" * 20)
        total_rows += chunk.shape[0]
        i+=1
    print(f"Succesfully wrote {total_rows} rows to table: green_taxi_2019\n")

    print("-" * 20)
    print(f"Writing {zones_df.shape[0]} rows to table: zones")

    # Write zones data to Postgres
    zones_df.to_sql("zones", con=connection, if_exists="replace")
    connection.commit()

    print(f"Succesfully wrote {zones_df.shape[0]} rows to table: zones")
