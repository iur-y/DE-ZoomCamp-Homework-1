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

# Create engine to establish connection with the Postgres database
engine = sqlalchemy.create_engine(f"postgresql://"
                                  f"{os.environ['POSTGRES_USER']}:"
                                  f"{os.environ['POSTGRES_PASSWORD']}@"
                                  "postgres_container:5432/"
                                  f"{os.environ['POSTGRES_DB']}")


# Establish the connection to start inserting data
with engine.connect() as connection:
    # Create a query to drop table with green taxi data if exists
    table_name = "green_september_2019"
    query = f"DROP TABLE IF EXISTS {table_name}"
    # Execute the drop table statement before writing
    connection.execute(sqlalchemy.text(query))
    connection.commit()

    i=0
    total_rows = 0
    print("-" * 20)
    # Write chunks to Postgres
    for chunk in green_df:
        print(f"Iteration {i}:\n")
        print(f"Writing {chunk.shape[0]} rows to table: {table_name} ...")
        chunk.to_sql(table_name, con=connection, if_exists="append")
        connection.commit()
        print("-" * 20)
        total_rows += chunk.shape[0]
        i+=1

    print(f"Succesfully wrote {total_rows} rows to {table_name}")

    # Create a query to drop zones table if exists
    table_name = "zones"
    query = f"DROP TABLE IF EXISTS {table_name}"
    # Execute the drop table statement before writing
    connection.execute(sqlalchemy.text(query))
    connection.commit()

    # Write zones data to Postgres
    print(f"Writing {zones_df.shape[0]} rows to table: {table_name}")
    zones_df.to_sql(table_name, con=connection, if_exists="replace")
    connection.commit()
    print(f"Succesfully wrote {zones_df.shape[0]} rows to {table_name}")
