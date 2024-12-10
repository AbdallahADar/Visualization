import pandas as pd
import numpy as np
import os
import pycountry

## US State and County
us_counties = pd.read_csv("geodata/us_county_names.csv")

## NUTS level Rates
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
os.makedirs("industry_rates", exist_ok = True)
os.makedirs("industry_rates/nuts", exist_ok = True)
os.makedirs("industry_rates/us_counties", exist_ok = True)

for i, name in zip(nuts3["NUTS3_ID"].values, nuts3["NUTS_NAME"].values):

    # Save files path
    os.makedirs(f"industry_rates/nuts/{i}", exist_ok = True)

    out1 = []
    out22 = []

    for j in sectors_ndy:

        sector = j["name"]
        rate = np.random.random(1)[0]        

        out2 = pd.DataFrame(j["industries"], columns = ["child"])
        out2["parent"] = sector
        out2["Count"] = np.random.uniform(0,100,len(out2)).astype(int)
        out2["Growth_Rate"] = np.random.random(len(out2))
        out2["Type"] = "Industry"
        out22.append(out2)

        out1.append([name, sector, out2["Count"].sum(), rate])
        
    out1 = pd.DataFrame(out1, columns = ["parent", "child", "Count", "Growth_Rate"])
    out1["Type"] = "Sector"

    out22 = pd.concat(out22)

    rate = np.random.random(1)[0]
    out3 = pd.DataFrame([["", name, out22["Count"].sum(), rate]], columns = ["parent", "child", "Count", "Growth_Rate"])
    out3["Type"] = "Overall"

    pd.concat([out3, out1, out22]).to_csv(f"industry_rates/nuts/{i}.csv", index = False)
        

for i, name in zip(us_counties["COUNTY_ID"].values, us_counties["COUNTY_NAME"].values):

    i = str(i) if len(str(i)) == 5 else "0"+str(i)

    # Save files path
    os.makedirs(f"industry_rates/us_counties/{i}", exist_ok = True)

    out1 = []
    out22 = []

    for j in sectors_ndy:

        sector = j["name"]
        rate = np.random.random(1)[0]

        out2 = pd.DataFrame(j["industries"], columns = ["child"])
        out2["parent"] = sector
        out2["Count"] = np.random.uniform(0,100,len(out2)).astype(int)
        out2["Growth_Rate"] = np.random.random(len(out2))
        out2["Type"] = "Industry"
        out22.append(out2)

        out1.append([name, sector, out2["Count"].sum(), rate])

    out1 = pd.DataFrame(out1, columns = ["parent", "child", "Count", "Growth_Rate"])
    out1["Type"] = "Sector"

    out22 = pd.concat(out22)

    rate = np.random.random(1)[0]
    out3 = pd.DataFrame([["", name, out22["Count"].sum(), rate]], columns = ["parent", "child", "Count", "Growth_Rate"])
    out3["Type"] = "Overall"

    pd.concat([out3, out1, out22]).to_csv(f"industry_rates/us_counties/{i}.csv", index = False)