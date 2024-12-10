import numpy as np
import pandas as pd
import pycountry
import requests
import os
import json

## Get ISO-2 Code for countries
countries = [country.alpha_2 for country in pycountry.countries]

## Get Data from the European Commission: 
# https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/
# We pull the geojson file from this website
# There are multiple versions of a file to choose from and the naming convention is:
# theme_spatialtype_resolution_year_projection_subset.format
# Useful resource for data explanation: https://gisco-services.ec.europa.eu/distribution/v2/nuts/nuts-2021-files.html
# theme for us is NUTS
# spatialtype can be BN (boundaries) or RG (regions) or LB (labels). We use regions.
# resolution: 60M/20M/10M/03M/01M; map scale the data is optimized (generalized) for. We use 01M.
# year is the year of the data
# projection: 4-digit EPSG code. We use 4326 (WGS84, coordinates in decimal degrees)
# subset: NUTS levels 0,1,2,3. No subset code means all NUTS levels are in the same file.
# LEVL_0: NUTS level 0 (countries)
# LEVL_1: NUTS level 1
# LEVL_2: NUTS level 2
# LEVL_3: NUTS level 3
# format is geojson for us

## Read in NUTS data as JSON file via API
def fetch_nuts_geojson(nuts_level, year, spatialtype = "RG", 
                       resolution = "01M", projection = 4326,
                       file_format = "geojson"):
    """
    Fetches the NUTS regions GeoJSON for Europe from an online resource.
    """

    # URL
    url = f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_{spatialtype}_{resolution}_{year}_{projection}_LEVL_{nuts_level}.{file_format}"
    response = requests.get(url)

    if response.status_code == 200: # Passed
        return response.json()
    else:
        print("Failed to retrieve NUTS1 GeoJSON data")
        return None

## Remove islands and territories since they cause issues in zoomed in maps
def exclude_islands_or_territories(features, country_code):
    """
    Excludes islands or territories based on country and specific NUTS codes.
    """
    # Define the NUTS codes or conditions to exclude specific regions
    exclusion_list = {
        "FR": ["FRY", "FRO"],  # Exclude French overseas territories
        "ES": ["ES7"],         # Exclude Canary Islands for Spain
        # Add more exclusions here for other countries if I find any.
    }

    if country_code in exclusion_list:
        return [feature for feature in features if not feature["properties"]["NUTS_ID"].startswith(tuple(exclusion_list[country_code]))]
    
    return features


## Get nuts data in clean format
def fetch_nuts_cleaned(nuts_level, year, spatialtype = "RG", 
                       resolution = "01M", projection = 4326,
                       file_format = "geojson"):

    nuts = fetch_nuts_geojson(nuts_level, year, spatialtype, 
                              resolution, projection, 
                              file_format)

    # Format it in desired format by groupping together regions within the country
    nuts = {
        country_code : [feature for feature in nuts["features"] if feature["properties"]["CNTR_CODE"] == country_code]
        for country_code in countries
    }
    
    # Remove countries with no data
    nuts = {i:j for i,j in nuts.items() if len(j) != 0}
    
    # Remove territories and islands
    nuts = {
        country_code : exclude_islands_or_territories(cf, country_code)
        for country_code, cf in nuts.items()
    }

    nuts_name_map = pd.DataFrame(
        [
            (country_code, feature["properties"]["NUTS_ID"], feature["properties"]["NAME_LATN"]) 
            for country_code, ff in nuts.items()
            for feature in ff
        ],
        columns = ["Country", "NUTS1_ID", "NUTS_NAME"])

    # Extra formatting for Level 2
    if nuts_level == 2:

        nuts_name_map.rename(columns = {"NUTS1_ID":"NUTS2_ID"}, inplace = True)
        nuts_name_map["NUTS1_ID"] = nuts_name_map["NUTS2_ID"].str[:3]
        
        
        nuts = {
            i: {
                j: {
                    k["properties"]["NUTS_ID"] : {
                        "type" : "Feature",
                        "properties" : k["properties"],
                        "geometry" : k["geometry"]
                        }
                    for k in nuts[i] if k["properties"]["NUTS_ID"][:3] == j[:3]
                    }
                for j in nuts_name_map[nuts_name_map["Country"] == i]["NUTS1_ID"].unique()
                }
            for i in nuts.keys()
            }

    elif nuts_level == 3:

        nuts_name_map.rename(columns = {"NUTS1_ID":"NUTS3_ID"}, inplace = True)
        nuts_name_map["NUTS1_ID"] = nuts_name_map["NUTS3_ID"].str[:3]
        nuts_name_map["NUTS2_ID"] = nuts_name_map["NUTS3_ID"].str[:4]

        nuts = {
            i : {
                j : {
                    k : {
                        l["properties"]["NUTS_ID"] : {
                            "type" : "Feature",
                            "properties" : l["properties"],
                            "geometry" : l["geometry"]
                            }
                        for l in nuts[i] if l["properties"]["NUTS_ID"][:4] == k[:4]
                        }
                    for k in nuts_name_map[nuts_name_map["NUTS1_ID"] == j]["NUTS2_ID"].unique()
                    }
                for j in nuts_name_map[nuts_name_map["Country"] == i]["NUTS1_ID"].unique()
                }
            for i in nuts.keys()
        }

    return nuts, nuts_name_map

## Save output as json
# Save each individual dict value as a separate json file for easy loading
# This way we wont have to carry a large variable during the app run
def save_at_level(data, base_dir, max_depth, depth=0, keys=None):
    """
    Recursively traverses a nested dictionary and saves data at a specified depth level.

    Args:
        data (dict): The nested dictionary to process.
        base_dir (str): The directory to save files.
        max_depth (int): The maximum depth to traverse before saving.
        depth (int): The current depth of traversal (default is 0).
        keys (list): The list of keys traversed so far (used for file naming).
    """
    if keys is None:
        keys = []
    
    if depth == max_depth:  # Save the current data if max depth is reached
        # Create nested directories based on the keys
        file_path = os.path.join(base_dir, *keys[:-1]) if len(keys) > 1 else base_dir
        os.makedirs(file_path, exist_ok=True)
        
        # Use the last key as the filename
        file_name = f"{keys[-1]}.json" if keys else "root.json"
        with open(os.path.join(file_path, file_name), "w") as f:
            json.dump(data, f, indent=4)
        return
    
    if isinstance(data, dict):  # If the current data is a dictionary, recurse
        for key, value in data.items():
            save_at_level(value, base_dir, max_depth, depth + 1, keys + [key])



# Get NUTS Data
nuts1, nuts1_names = fetch_nuts_cleaned(1, 2024)
nuts2, nuts2_names = fetch_nuts_cleaned(2, 2024)
nuts3, nuts3_names = fetch_nuts_cleaned(3, 2024)

# Save files path
os.makedirs("geodata", exist_ok = True)

# Add ISO 3 Code
nuts1_names["Country"] = nuts1_names["Country"].apply(lambda x: pycountry.countries.get(alpha_2 = x).alpha_3)
nuts2_names["Country"] = nuts2_names["Country"].apply(lambda x: pycountry.countries.get(alpha_2 = x).alpha_3)
nuts3_names["Country"] = nuts3_names["Country"].apply(lambda x: pycountry.countries.get(alpha_2 = x).alpha_3)

# Save naming files as csv
nuts1_names.to_csv("geodata/nuts1_names.csv", index = False)
nuts2_names.to_csv("geodata/nuts2_names.csv", index = False)
nuts3_names.to_csv("geodata/nuts3_names.csv", index = False)

# Save dict as separate json files
save_at_level(nuts1, "geodata/nuts1", 1)
save_at_level(nuts2, "geodata/nuts2", 2)
save_at_level(nuts3, "geodata/nuts3", 3)


## Get US Counties Data

fips_codes_state_full = {
    "Alabama": "01",
    "Alaska": "02",
    "Arizona": "04",
    "Arkansas": "05",
    "California": "06",
    "Colorado": "08",
    "Connecticut": "09",
    "Delaware": "10",
    "District of Columbia": "11",
    "Florida": "12",
    "Georgia": "13",
    "Hawaii": "15",
    "Idaho": "16",
    "Illinois": "17",
    "Indiana": "18",
    "Iowa": "19",
    "Kansas": "20",
    "Kentucky": "21",
    "Louisiana": "22",
    "Maine": "23",
    "Maryland": "24",
    "Massachusetts": "25",
    "Michigan": "26",
    "Minnesota": "27",
    "Mississippi": "28",
    "Missouri": "29",
    "Montana": "30",
    "Nebraska": "31",
    "Nevada": "32",
    "New Hampshire": "33",
    "New Jersey": "34",
    "New Mexico": "35",
    "New York": "36",
    "North Carolina": "37",
    "North Dakota": "38",
    "Ohio": "39",
    "Oklahoma": "40",
    "Oregon": "41",
    "Pennsylvania": "42",
    "Rhode Island": "44",
    "South Carolina": "45",
    "South Dakota": "46",
    "Tennessee": "47",
    "Texas": "48",
    "Utah": "49",
    "Vermont": "50",
    "Virginia": "51",
    "Washington": "53",
    "West Virginia": "54",
    "Wisconsin": "55",
    "Wyoming": "56",
    "Puerto Rico": "72"
}

fips_codes_state_code = {
    "AL": "01",  # Alabama
    "AK": "02",  # Alaska
    "AZ": "04",  # Arizona
    "AR": "05",  # Arkansas
    "CA": "06",  # California
    "CO": "08",  # Colorado
    "CT": "09",  # Connecticut
    "DE": "10",  # Delaware
    "DC": "11",  # District of Columbia
    "FL": "12",  # Florida
    "GA": "13",  # Georgia
    "HI": "15",  # Hawaii
    "ID": "16",  # Idaho
    "IL": "17",  # Illinois
    "IN": "18",  # Indiana
    "IA": "19",  # Iowa
    "KS": "20",  # Kansas
    "KY": "21",  # Kentucky
    "LA": "22",  # Louisiana
    "ME": "23",  # Maine
    "MD": "24",  # Maryland
    "MA": "25",  # Massachusetts
    "MI": "26",  # Michigan
    "MN": "27",  # Minnesota
    "MS": "28",  # Mississippi
    "MO": "29",  # Missouri
    "MT": "30",  # Montana
    "NE": "31",  # Nebraska
    "NV": "32",  # Nevada
    "NH": "33",  # New Hampshire
    "NJ": "34",  # New Jersey
    "NM": "35",  # New Mexico
    "NY": "36",  # New York
    "NC": "37",  # North Carolina
    "ND": "38",  # North Dakota
    "OH": "39",  # Ohio
    "OK": "40",  # Oklahoma
    "OR": "41",  # Oregon
    "PA": "42",  # Pennsylvania
    "RI": "44",  # Rhode Island
    "SC": "45",  # South Carolina
    "SD": "46",  # South Dakota
    "TN": "47",  # Tennessee
    "TX": "48",  # Texas
    "UT": "49",  # Utah
    "VT": "50",  # Vermont
    "VA": "51",  # Virginia
    "WA": "53",  # Washington
    "WV": "54",  # West Virginia
    "WI": "55",  # Wisconsin
    "WY": "56",  # Wyoming
    "PR": "72"   # Puerto Rico
}

us_state_names = pd.DataFrame(fips_codes_state_code.keys(), columns = ["State"])
us_state_names["FIPS"] = us_state_names["State"].map(fips_codes_state_code)
us_state_names["States_Full"] = us_state_names["FIPS"].map({j:i for i,j in fips_codes_state_full.items()})
# Save naming file as csv
us_state_names.to_csv("geodata/us_state_names.csv", index = False)

# Retrieve Counties geo data
def fetch_counties_geojson(county_code_map = fips_codes_state_code):

    ## Get counties geojson
    r = requests.get('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
    counties = json.loads(r.text)

    ## Convert data into dict form
    ret = {
        n : [f for f in counties['features'] if f['properties']['STATE'] == i]
        for n,i in county_code_map.items()
        }

    county_names = pd.DataFrame(
        [
            (state, feature["properties"]["STATE"] + feature["properties"]["COUNTY"], feature["properties"]["NAME"], feature["properties"]["STATE"]) 
            for state, ff in ret.items()
            for feature in ff
            ],
        columns = ["State", "COUNTY_ID", "COUNTY_NAME", "STATE_FIPS"])

    return ret, county_names


us_counties, us_counties_names = fetch_counties_geojson()

# Save naming file as csv
us_counties_names.to_csv("geodata/us_county_names.csv", index = False)

# Save dict as separate json files
save_at_level(us_counties, "geodata/us_counties", 1)