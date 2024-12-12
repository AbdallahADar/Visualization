import pandas as pd
import numpy as np
import os
import pycountry

## Sectors
SECTORS = ["HiTech", "Agriculture", "Transportation", "Consumer_Products", "Unassigned", "Communication", "Trade", "Business_Services", "Business_Products", "Construction", "Services", "Mining", "Health_Care", "EnergyExpL_Prod", "Utilities"]

## Covered countries
COVERED_COUNTRIES = [
    "ALB", "AUS", "AUT", "BEL", "BGR", "COL", "ESP", "FIN", "FRA", "HUN", "ITA", "KOR", "MDA", "NZL", "POL", "PRT", "ROU", "RUS", "SRB", "SVK", "SWE", "THA", "UKR", "USA", "VNM", "DEU", "DNK", "GBR", "IDN", "ISL", "JPN", "LVA", "MEX", "MYS", "PHL", "SVN", "ZAF", "CAN", "CHE", "CZE", "DZA", "EST", "HRV", "ISR", "LTU", "SGP", "TWN", "MKD", "NOR", "BIH", "LUX", "NLD", "PAK", "GRC", "KAZ", "MNE", "BRA", "IND", "TUR", "IRN", "MAR", "HKG", "MLT"
]
countries = pd.DataFrame({"Country" : [i for i in COVERED_COUNTRIES]})

## US State and County
us_state = pd.read_csv("geodata/us_state_names.csv")
us_counties = pd.read_csv("geodata/us_county_names.csv")

## NUTS level Rates
nuts1 = pd.read_csv("geodata/nuts1_names.csv")
nuts2 = pd.read_csv("geodata/nuts2_names.csv")
nuts3 = pd.read_csv("geodata/nuts3_names.csv")

# Save files path
os.makedirs("geo_rates", exist_ok = True)

for sector in SECTORS:
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