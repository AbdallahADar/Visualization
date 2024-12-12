import pandas as pd
import numpy as np
import os
import pycountry

## Countries
countries = pd.DataFrame({"Country" : [country.alpha_3 for country in pycountry.countries]})

## US State and County
us_state = pd.read_csv("geodata/us_state_names.csv")
us_counties = pd.read_csv("geodata/us_county_names.csv")

## NUTS level Rates
nuts1 = pd.read_csv("geodata/nuts1_names.csv")
nuts2 = pd.read_csv("geodata/nuts2_names.csv")
nuts3 = pd.read_csv("geodata/nuts3_names.csv")

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

# Save files path
os.makedirs("geo_rates", exist_ok = True)

for i in sectors_ndy:

    sector = i["name"]

    # Save files path
    os.makedirs(f"geo_rates/{sector}/", exist_ok = True)

    ## Add randomized growth rates
    us_state["Growth_Rate"] = np.random.random(len(us_state))
    us_counties["Growth_Rate"] = np.random.random(len(us_counties))
    nuts1["Growth_Rate"] = np.random.random(len(nuts1))
    nuts2["Growth_Rate"] = np.random.random(len(nuts2))
    nuts3["Growth_Rate"] = np.random.random(len(nuts3))
    countries["Growth_Rate"] = np.random.random(len(countries))
    

    ## Save files for each sector separately
    us_state.to_csv(f"geo_rates/{sector}/us_state.csv", index = False)
    us_counties.to_csv(f"geo_rates/{sector}/us_county.csv", index = False)
    nuts1.to_csv(f"geo_rates/{sector}/nuts1.csv", index = False)
    nuts2.to_csv(f"geo_rates/{sector}/nuts2.csv", index = False)
    nuts3.to_csv(f"geo_rates/{sector}/nuts3.csv", index = False)
    countries.to_csv(f"geo_rates/{sector}/countries.csv", index = False)

    ## Add randomized growth rate for industry
    for j in i["industries"]:

        # Save files path
        os.makedirs(f"geo_rates/{sector}/{j}/", exist_ok = True)

        ## Add randomized growth rates
        us_state["Growth_Rate"] = np.random.random(len(us_state))
        us_counties["Growth_Rate"] = np.random.random(len(us_counties))
        nuts1["Growth_Rate"] = np.random.random(len(nuts1))
        nuts2["Growth_Rate"] = np.random.random(len(nuts2))
        nuts3["Growth_Rate"] = np.random.random(len(nuts3))
        countries["Growth_Rate"] = np.random.random(len(countries))

        ## Save files for each sector+ndy separately
        us_state.to_csv(f"geo_rates/{sector}/{j}/us_state.csv", index = False)
        us_counties.to_csv(f"geo_rates/{sector}/{j}/us_county.csv", index = False)
        nuts1.to_csv(f"geo_rates/{sector}/{j}/nuts1.csv", index = False)
        nuts2.to_csv(f"geo_rates/{sector}/{j}/nuts2.csv", index = False)
        nuts3.to_csv(f"geo_rates/{sector}/{j}/nuts3.csv", index = False)
        countries.to_csv(f"geo_rates/{sector}/{j}/countries.csv", index = False)


# All sector data
sector = "All"

# Save files path
os.makedirs(f"geo_rates/{sector}/", exist_ok = True)

## Add randomized growth rates
us_state["Growth_Rate"] = np.random.random(len(us_state))
us_counties["Growth_Rate"] = np.random.random(len(us_counties))
nuts1["Growth_Rate"] = np.random.random(len(nuts1))
nuts2["Growth_Rate"] = np.random.random(len(nuts2))
nuts3["Growth_Rate"] = np.random.random(len(nuts3))
countries["Growth_Rate"] = np.random.random(len(countries))


## Save files for each sector separately
us_state.to_csv(f"geo_rates/{sector}/us_state.csv", index = False)
us_counties.to_csv(f"geo_rates/{sector}/us_county.csv", index = False)
nuts1.to_csv(f"geo_rates/{sector}/nuts1.csv", index = False)
nuts2.to_csv(f"geo_rates/{sector}/nuts2.csv", index = False)
nuts3.to_csv(f"geo_rates/{sector}/nuts3.csv", index = False)
countries.to_csv(f"geo_rates/{sector}/countries.csv", index = False)