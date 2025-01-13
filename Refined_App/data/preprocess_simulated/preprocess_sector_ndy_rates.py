import pandas as pd
import numpy as np
import os
import pycountry

## US State and County
us_counties = pd.read_csv("geodata/us_county_names.csv")

## NUTS level Rates
nuts3 = pd.read_csv("geodata/nuts3_names.csv")

## Sector and Industries
SECTORS = ["HiTech", "Agriculture", "Transportation", "Consumer_Products", "Unassigned", "Communication", "Trade", "Business_Services", "Business_Products", "Construction", "Services", "Mining", "Health_Care", "EnergyExpL_Prod", "Utilities"]

# Save files path
os.makedirs("industry_rates", exist_ok = True)
os.makedirs("industry_rates/nuts", exist_ok = True)
os.makedirs("industry_rates/us_counties", exist_ok = True)
os.makedirs(f"industry_rates/countries/", exist_ok = True)

for i, name in zip(nuts3["NUTS3_ID"].values, nuts3["NUTS_NAME"].values):

    out1 = []

    for sector in SECTORS:
        out1.append([name, sector, np.random.uniform(0,100,1).astype(int)[0], np.random.random(1)[0]])
        
    out1 = pd.DataFrame(out1, columns = ["parent", "child", "Count", "Growth_Rate"])
    out1["Type"] = "Sector"

    rate = out1["Growth_Rate"].mean()
    out3 = pd.DataFrame([["", name, out1["Count"].sum(), rate]], columns = ["parent", "child", "Count", "Growth_Rate"])
    out3["Type"] = "Overall"

    pd.concat([out3, out1]).to_csv(f"industry_rates/nuts/{i}.csv", index = False)
        

for i, name in zip(us_counties["COUNTY_ID"].values, us_counties["COUNTY_NAME"].values):

    i = str(i) if len(str(i)) == 5 else "0"+str(i)

    out1 = []

    for sector in SECTORS:
        out1.append([name, sector, np.random.uniform(0,100,1).astype(int)[0], np.random.random(1)[0]])

    out1 = pd.DataFrame(out1, columns = ["parent", "child", "Count", "Growth_Rate"])
    out1["Type"] = "Sector"

    rate = out1["Growth_Rate"].mean()
    out3 = pd.DataFrame([["", name, out1["Count"].sum(), rate]], columns = ["parent", "child", "Count", "Growth_Rate"])
    out3["Type"] = "Overall"

    pd.concat([out3, out1]).to_csv(f"industry_rates/us_counties/{i}.csv", index = False)
    
COVERED_COUNTRIES = [
    "ALB", "AUS", "AUT", "BEL", "BGR", "COL", "ESP", "FIN", "FRA", "HUN", "ITA", "KOR", "MDA", "NZL", "POL", "PRT", "ROU", "RUS", "SRB", "SVK", "SWE", "THA", "UKR", "USA", "VNM", "DEU", "DNK", "GBR", "IDN", "ISL", "JPN", "LVA", "MEX", "MYS", "PHL", "SVN", "ZAF", "CAN", "CHE", "CZE", "DZA", "EST", "HRV", "ISR", "LTU", "SGP", "TWN", "MKD", "NOR", "BIH", "LUX", "NLD", "PAK", "GRC", "KAZ", "MNE", "BRA", "IND", "TUR", "IRN", "MAR", "HKG", "MLT"
]

for i in COVERED_COUNTRIES:
    
    out1 = []

    for sector in SECTORS:
        out1.append([i, sector, np.random.uniform(0,100,1).astype(int)[0], np.random.random(1)[0]])

    out1 = pd.DataFrame(out1, columns = ["parent", "child", "Count", "Growth_Rate"])
    out1["Type"] = "Sector"

    rate = out1["Growth_Rate"].mean()
    out3 = pd.DataFrame([["", i, out1["Count"].sum(), rate]], columns = ["parent", "child", "Count", "Growth_Rate"])
    out3["Type"] = "Overall"

    pd.concat([out3, out1]).to_csv(f"industry_rates/countries/{i}.csv", index = False)