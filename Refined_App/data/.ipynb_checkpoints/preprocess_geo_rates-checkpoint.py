import numpy as np
import pandas as pd
import os
import pycountry

countries = pd.read_csv("loaded_data/growth_rate_2010onwards.csv")

## Sectors
SECTORS = ["HiTech", "Agriculture", "Transportation", "Consumer_Products", "Unassigned", "Communication", "Trade", "Business_Services", "Business_Products", "Construction", "Services", "Mining", "Health_Care", "EnergyExpL_Prod", "Utilities"]

# Save files path
os.makedirs("geo_rates", exist_ok = True)

for sector in SECTORS + ["All"]:
    # Save files path
    os.makedirs(f"geo_rates/{sector}/", exist_ok = True)

    countries[countries["Sector"] == sector].to_csv(f"geo_rates/{sector}/countries.csv", index = False)