import numpy as np
import pandas as pd
import pycountry
import random
import os

# Get a list of all country codes from ISO 3166-1 using pycountry
countries = list(set([country.alpha_3 for country in pycountry.countries]) - 
     set(["ABW", "AGO", "AND", "AZE","BMU","BRB","CAF","CIV","CUB","CUW","FLK", "FJI",
         "IMN","STP","GIB","NIU","COD","IOT","ERI","KWT","GIN","GUM","NCL","GHA"]))

## NUTS Countries
nuts_countries = [
    "AUT",  # Austria
    "BEL",  # Belgium
    "BGR",  # Bulgaria
    "HRV",  # Croatia
    "CYP",  # Cyprus
    "CZE",  # Czech Republic
    "DNK",  # Denmark
    "EST",  # Estonia
    "FIN",  # Finland
    "FRA",  # France
    "DEU",  # Germany
    "GRC",  # Greece
    "HUN",  # Hungary
    "IRL",  # Ireland
    "ITA",  # Italy
    "LVA",  # Latvia
    "LTU",  # Lithuania
    "LUX",  # Luxembourg
    "MLT",  # Malta
    "NLD",  # Netherlands
    "POL",  # Poland
    "PRT",  # Portugal
    "ROU",  # Romania
    "SVK",  # Slovakia
    "SVN",  # Slovenia
    "ESP",  # Spain
    "SWE",  # Sweden
    "NOR",  # Norway
    "CHE",  # Switzerland
    "ISL",  # Iceland
    "LI",   # Liechtenstein
]

non_granular_countries = list(set(countries) - set(nuts_countries + ["USA"]))

# Size options
sizes = ['Large', 'Medium', 'Small', 'Micro']

## Sector and Industries
sectors_ndy = [
    {"name": "Technology", "industries": ["Software", "Hardware", "IT Services"]},
    {"name": "Healthcare", "industries": ["Pharmaceuticals", "Medical Devices", "Healthcare Services"]},
    {"name": "Finance", "industries": ["Banking", "Insurance", "Investment Services"]},
    {"name": "Energy", "industries": ["Oil & Gas", "Renewable Energy", "Energy Exploration"]},
    {"name": "Consumer Goods", "industries": ["Food & Beverage", "Household Products", "Apparel"]},
    {"name": "Utilities", "industries": ["Electric", "Water", "Gas"]},
    {"name": "Real Estate", "industries": ["Residential", "Commercial", "Industrial"]},
    {"name": "Telecommunications", "industries": ["Mobile", "Broadband", "Satellite"]},
    {"name": "Materials", "industries": ["Chemicals", "Metals & Mining", "Construction Materials"]},
    {"name": "Industrials", "industries": ["Aerospace & Defense", "Machinery", "Industrial Services"]},
    {"name": "Consumer Services", "industries": ["Retail", "Travel & Leisure", "Media"]},
    {"name": "Transportation", "industries": ["Airlines", "Railroads", "Logistics"]}
]

# Create Data for Countries with Only Country Level Data
data = []
for country in non_granular_countries:
    for size in sizes:
        for i in sectors_ndy:
            sector = i["name"]
            for ndy in i["industries"]:
                nobs = np.random.randint(5,50)
                for n in range(nobs):
                    data.append([country, size, sector, ndy, country])


df_non_granular = pd.DataFrame(data, columns = ["Country", "Size", "Sector", "Industry", "Location"])

# Create data for NUTS Countries
df_nuts3 = pd.read_csv("geodata/nuts3_names.csv")
df_nuts2 = pd.read_csv("geodata/nuts2_names.csv")
df_nuts1 = pd.read_csv("geodata/nuts1_names.csv")

nuts = (
    df_nuts3
    .merge(df_nuts2.drop(columns = ["NUTS1_ID"]), 
           how = "left",
           on = "NUTS2_ID"
          )
    .merge(df_nuts1, 
           how = "left",
           on = "NUTS1_ID")
    .assign(Location=lambda x: x["NUTS_NAME_x"] + ", " + x["NUTS_NAME_y"] + ", " + x["NUTS_NAME"] + ", " + x["Country"])
)[["Country", "Location", "NUTS3_ID"]]

data2 = []
for geo in nuts["NUTS3_ID"].unique():
    for size in sizes:
        for i in sectors_ndy:
            sector = i["name"]
            for ndy in i["industries"]:
                nobs = np.random.randint(5,50)
                for n in range(nobs):
                    data2.append([geo, size, sector, ndy])

df_nuts = (
    pd.DataFrame(data2, columns = ["NUTS3_ID", "Size", "Sector", "Industry"])
    .merge(nuts, how = "left", on = "NUTS3_ID")
)

# Create Data for USA
df_counties = pd.read_csv("geodata/us_county_names.csv")
df_counties["Location"] = df_counties["COUNTY_NAME"] + ", " + df_counties["State"] + ", USA"
df_counties["Country"] = "USA"

data3 = []
for geo in df_counties["COUNTY_ID"].unique():
    for size in sizes:
        for i in sectors_ndy:
            sector = i["name"]
            for ndy in i["industries"]:
                nobs = np.random.randint(5,50)
                for n in range(nobs):
                    data3.append([geo, size, sector, ndy])

df_us = (
    pd.DataFrame(data3, columns = ["COUNTY_ID", "Size", "Sector", "Industry"])
    .merge(df_counties[["Location", "COUNTY_ID", "Country", "State"]], how = "left", on = "COUNTY_ID")
)

# Propensity flags
flags = [True, False]
ews_label = ["Low", "Medium", "High", "Severe"]
ratings = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa/C"]

df_full = pd.concat([df_non_granular, df_nuts, df_us])
df_full["Name"] = [f"Name{i}" for i in range(len(df_full))]
df_full["Growth"] = random.choices(flags, k = len(df_full))
df_full["Borrow"] = random.choices(flags, k = len(df_full))
df_full["Shrink"] = random.choices(flags, k = len(df_full))
df_full["Shrink"] = df_full.apply(lambda x: False if x["Growth"] == True else x["Shrink"], axis = 1)
df_full["IR"] = random.choices(ratings, k = len(df_full))

df_full["EWS"] = random.choices(ews_label, k = len(df_full))

df_full = df_full[(df_full["Growth"]==True) | (df_full["Borrow"]==True) | (df_full["Shrink"]==True)]

# Save files path
os.makedirs("sample_data", exist_ok = True)

import os
import pandas as pd

def save_csv_partitions(df, base_directory, partition_cols, file_name="data.csv"):
    """
    Save a DataFrame into CSV files organized in a nested directory structure based on specified partition columns.

    Parameters:
    - df: pd.DataFrame - The DataFrame to partition and save.
    - base_directory: str - The root directory for saving files.
    - partition_cols: list - List of column names to partition by.
    - file_name: str - Name of the CSV file to save in each partition directory.
    """
    if not partition_cols:
        raise ValueError("You must specify at least one column to partition by.")

    # Group by the specified columns
    for partition_values, subset in df.groupby(partition_cols):
        # Create directory structure based on partition columns and values
        partition_path = os.path.join(
            base_directory, 
            *[f"{col}={val}" for col, val in zip(partition_cols, partition_values)]
        )
        os.makedirs(partition_path, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Save the subset as a CSV file in the directory
        file_path = os.path.join(partition_path, file_name)
        subset.to_csv(file_path, index=False)

    print(f"Data saved in partitions under {base_directory}")



## Save parquet files
# df_full[df_full["COUNTY_ID"].notna()].to_parquet("sample_data", 
#                                                  engine="pyarrow",
#                                                  partition_cols=["Country", "State", "COUNTY_ID"])

# df_full[df_full["NUTS3_ID"].notna()].to_parquet("sample_data", 
#                                                  engine="pyarrow",
#                                                  partition_cols=["Country", "NUTS3_ID"])

# df_full[(df_full["NUTS3_ID"].notna()) & (df_full["COUNTY_ID"].notna())].to_parquet("sample_data", 
#                                                  engine="pyarrow",
#                                                  partition_cols=["Country"])


save_csv_partitions(df_full[df_full["COUNTY_ID"].notna()].copy(), 
                    base_directory="sample_data", partition_cols=["Country", "State", "COUNTY_ID"])

save_csv_partitions(df_full[df_full["NUTS3_ID"].notna()].copy(), 
                    base_directory="sample_data", partition_cols=["Country", "NUTS3_ID"])

save_csv_partitions(df_full[(df_full["NUTS3_ID"].isna()) & (df_full["COUNTY_ID"].isna())].copy(), 
                    base_directory="sample_data", partition_cols=["Country"])




















