import numpy as np
import pandas as pd
import itertools
import random
import Geographical_Plots as GPlots
import pycountry
import us
from functools import reduce
from itertools import combinations, permutations, product

################ METADATA & FORMATTING ################

narrative = '''This firm belongs in the high propensity for growth and medium propensity for borrowing while belonging to the resilient risk segment. Such firms need liquidity to continue to fuel their growth trajectory. Belonging to the resilient segment ensures that the company is suitable to endure different economic conditions and remain low risk. These companies would serve as good partners to enhance existing relationships or build long term relationships.
'''

## Table styling
# Cell styling rules for conditional coloring
cell_styling_func = [
    {"condition": "params.value === '1High'", "style": {"backgroundColor": "#0046BF", 'color': '#0046BF'}},
    {"condition": "params.value === '2Medium-High'", "style": {"backgroundColor": "#669EFF", 'color': '#669EFF'}},
    {"condition": "params.value === '3Medium-Low'", "style": {"backgroundColor": "#99BFFF", 'color': '#99BFFF'}},
    {"condition": "params.value === '4Low'", "style": {"backgroundColor": "#CCDFFF", 'color': '#CCDFFF'}},
]

## Start page styling

exploratory_half = {
    'flex': '1', 
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center',
    'background-color': '#007BFF', 
    'cursor': 'pointer', 
    'transition': 'flex 0.6s ease',
    'position': 'relative', 
    'height': '100%'
    }

targeted_half = {
    'flex': '1', 
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center',
    'background-color': '#28A745', 
    'cursor': 'pointer', 
    'transition': 'flex 0.6s ease',
    'position': 'relative', 
    'height': '100%'
    }

## Geographical figure styling
geofig_styling = {
    'display': 'flex',
    'justifyContent': 'center',  # Horizontally center the graph
    'alignItems': 'center', # Vertically center the graph
    'margin-bottom':'5px',
    # 'marginLeft': 'auto', 'marginRight': 'auto'
}

## Hot zone toggle contianer overall
hotzone_toggle = {
    'display': 'flex', 
    'justify-content': 'center', 
    'padding': '5px', 
    'margin-bottom': '5px', 
    'margin-top': '5px'
}

## Create risk segment metadata
category_risk = ["Green", "Yellow", "Orange", "Red"]
naming = ["Ultra-Resilient", "Very Resileint", "Resilient", "Sensitive", "Elevated Risk", "Resurgent", "Distressed",
         "Emerging Risk", "Critical Risk", "Vulnerable", "Fragile", "Exposed"] * 22

# Get all possible combinations of 4 from the list
combinations = list(itertools.product(category_risk, repeat = 4))
segment_names = {";".join(i) :naming[n]  for n,i in enumerate(combinations)}

# Define the color mapping and position mapping for risk segmentation
color_mapping_risk = {'Red': '#FF4136', 'Orange': '#FF851B', 'Yellow': '#FFDC00', 'Green': '#2ECC40'}
position_mapping_risk = {'Red': 0.25, 'Orange': 0.5, 'Yellow': 0.75, 'Green': 1.0}

# Order of scenarios
scenario_order_risk = ["", "s0", "bl", "s1"]

# Label of scenarios
scenario_label_risk = ["Current", "Upside", "Baseline", "Downside"]

# Growth rates metadata
growth_metadata = pd.DataFrame(
    {
        "Country" : ["USA"]*13 + ["GBR"]*13 + ["Global"]*13 + ["ESP"]*13 + ["FRA"]*13 + ["DEU"]*13 + ["ITA"]*13 + ["BRA"]*13,
        "Sector" : ['Technology','Healthcare','Finance','Energy','Consumer Goods','Utilities','Real Estate',
                    'Telecommunications','Materials','Industrials','Consumer Services','Transportation', 'All'] * 8,
        "Count" : np.random.randint(10_000, 1_000_000, 104),
        "Growth Rate" : np.random.uniform(0,1,104)
    }
)

# Example Percentile Map
percentiles_sales = pd.DataFrame(
    {"perc": range(0, 101),
     "A": list(itertools.chain(range(20,0,-1) ,range(81))),
     "B": range(0, 101),
     "C": list(itertools.chain(range(20,50), range(50, 30, -1), range(30, 81))),
     "D": list(itertools.chain(range(50), range(50, 30, -1), range(30, 61))),
     "E": list(itertools.chain(range(40,20,-1), range(20, 51), range(50, 0, -1))),
     "F": list(itertools.chain(range(81,20,-1), range(20, 60))),
     "G": list(itertools.chain(range(70), range(70, 39, -1)))})

percentiles_asset = pd.DataFrame(
    {"perc": range(0, 101),
     "A": list(itertools.chain(range(20,0,-1) ,range(81))),
     "B": range(0, 101),
     "C": list(itertools.chain(range(20,50), range(50, 30, -1), range(30, 81))),
     "D": range(100,-1,-1),
     "E": list(itertools.chain(range(40,20,-1), range(20, 51), range(50, 0, -1))),
     "F": list(itertools.chain(range(61,20,-1), range(20, 80))),
     "G": list(itertools.chain(range(70), range(70, 39, -1)))})

percentiles_shrink = pd.DataFrame(
    {"perc": range(0, 101),
     "A": list(itertools.chain(range(20,0,-1) ,range(81))),
     "B": range(0, 101),
     "C": list(itertools.chain(range(20,50), range(50, 30, -1), range(30, 81))),
     "D": range(101),
     "E": list(itertools.chain(range(40,10,-1), range(10, 41), range(40, 0, -1))),
     "F": list(itertools.chain(range(81,20,-1), range(20, 60))),
     "G": list(itertools.chain(range(70), range(70, 39, -1)))})

percentiles_borrow = pd.DataFrame(
    {"perc": range(0, 101),
     "A": list(itertools.chain(range(20,0,-1) ,range(81))),
     "B": range(0, 101),
     "C": list(itertools.chain(range(20,50), range(50, 30, -1), range(30, 81))),
     "D": list(itertools.chain(range(90), range(90, 79, -1))),
     "E": list(itertools.chain(range(40,20,-1), range(20, 51), range(50, 0, -1))),
     "F": list(itertools.chain(range(91,20,-1), range(20, 50))),
     "G": list(itertools.chain(range(70), range(70, 39, -1)))})

model_type_list = ["Sales", "Asset", "Borrow", "Shrink"]

percentiles_full = {"Sales" : percentiles_sales,
                    "Asset" : percentiles_asset,
                    "Shrink" : percentiles_shrink,
                    "Borrow" : percentiles_borrow}

# Color maps
color_hex_101 = ["#A50026", "#AA0426", "#AF0926", "#B40E26", "#B91326", "#BE1826", "#C31C26", "#C82126", "#CD2626", "#D22B26", "#D73027", "#D93629",
                 "#DC3C2C", "#DF422F", "#E24832", "#E54E34", "#E85437", "#EB5A3A", "#EE603D", "#F16640", "#F46D43", "#F47345", "#F57949", "#F6804C",
                 "#F7864E", "#F88D51", "#F99355", "#FA9A58", "#FBA15A", "#FCA75D", "#FDAD60", "#FDB365", "#FDB869", "#FDBC6D", "#FDC271", "#FDC775",
                 "#FDCB7A", "#FDD17E", "#FDD582", "#FDDB86", "#FEE08B", "#FEE390", "#FEE695", "#FEE99A", "#FEEC9F", "#FEEFA4", "#FEF2AA", "#FEF5AF",
                 "#FEF8B4", "#FEFBB9", "#FFFFBF", "#FBFDB9", "#F7FBB4", "#F3FAAF", "#EFF8AA", "#ECF7A4", "#E8F59F", "#E4F39A", "#E0F295", "#DCF090",
                 "#D9EF8B", "#D3EC87", "#CEEA84", "#C9E881", "#C4E67D", "#BFE47A", "#BAE177", "#B5DF73", "#B0DD70", "#ABDB6D", "#A6D96A", "#9FD669",
                 "#99D368", "#92D067", "#8CCD67", "#86CB66", "#7FC865", "#79C565", "#72C264", "#6CBF63", "#66BD63", "#5EB961", "#56B55F", "#4FB15D",
                 "#47AE5B", "#40AA59", "#38A657", "#30A355", "#299F53", "#219B51", "#1A9850", "#17934D", "#148E4A", "#128948", "#0F8445", "#0C7F43",
                 "#0A7B41", "#07763E", "#05713C", "#026C39", "#006837"]

color_hex_df = pd.DataFrame(enumerate(color_hex_101))

custom_color_map_101 = [[i,j] for i,j in zip(np.linspace(0,1,len(color_hex_101)),color_hex_101)]

# Define category colors
category_colors = {
    'Green': '#0046BF',
    'Yellow': '#669EFF',
    'Red': '#CCDFFF',
    'Orange': '#99BFFF',
    'Selected': '#000000'  # Black for selected state
}

category_colors_labels = {
    'H': '#0046BF',
    'MH': '#669EFF',
    'L': '#CCDFFF',
    'ML': '#99BFFF',
}

category_colors_labels_full = {
    'High': '#0046BF',
    'Medium-High': '#669EFF',
    'Low': '#CCDFFF',
    'Medium-Low': '#99BFFF',
}

# Ratio categories
ratio_categories = {
    "A" : "Profitability",
    "B": "Profitability",
    "C":"Leverage",
    "D":"Liquidity",
    "E":"Liquidity",
    "F" : "Grow",
    "G" : "Grow"
}

# To sort dataframe by custom category order
category_order = {'Green': 0, 'Yellow': 1, 'Red': 3, 'Orange': 2}

############# Full Scored Dataset #############

np.random.seed(18)
# Create a sample dataframe including additional line items for each company
# Fixing the incomplete input for the final attempt

df = pd.DataFrame({
    'Names': [f'Name{i}' for i in range(1, 101)],
    # 'Category': ['Green', 'Yellow', 'Red', 'Orange'] * 6 + ['Green'],
    'Sales': [1000 + i * 100 for i in np.random.randn(100)],
    'Asset': [2000 + i * 150 for i in np.random.randn(100)],
    'Sector': ['Technology', 'Finance', 'Energy', 'Healthcare', "Consumer Goods", 'Utilities', 
               'Real Estate', 'Telecommunications', 'Materials', 'Industrials', 'Consumer Services',
               'Transportation'] * 8 + ['Technology', 'Finance', 'Energy', 'Healthcare'],
    'Country': ['USA', 'CAN', 'DEU', 'GBR', 'ESP', 'FRA', 'ITA', 'BEL', 'MYS', 'PRT'] * 10,
    'Size': ['Large', 'Medium', 'Small', 'Micro'] * 25,
    'SalesP': [10 + i for i in np.random.randint(0, 75, 100)],
    'AssetP': [15 + i for i in np.random.randint(0, 55, 100)],
    'ShrinkP': [5 + i for i in np.random.randint(0, 65, 100)],
    'BorrowP': [80 - i for i in np.random.randint(0, 75, 100)],
    'Sales_1': [950 + i * 100 for i in np.random.randn(100)],
    'Sales_2': [900 + i * 100 for i in np.random.randn(100)],
    'Sales_3': [850 + i * 100 for i in np.random.randn(100)],
    'Sales_4': [800 + i * 100 for i in np.random.randn(100)],
    'Sales_5': [750 + i * 100 for i in np.random.randn(100)],
    'Asset_1': [1950 + i * 100 for i in np.random.randn(100)],
    'Asset_2': [1800 + i * 100 for i in np.random.randn(100)],
    'Asset_3': [1700 + i * 100 for i in np.random.randn(100)],
    'Asset_4': [1600 + i * 100 for i in np.random.randn(100)],
    'Asset_5': [1500 + i * 100 for i in np.random.randn(100)],
    "A_Sales": np.random.uniform(0, 100, 100),
    "B_Sales": np.random.uniform(0, 100, 100),
    "C_Sales": np.random.uniform(0, 100, 100),
    "D_Sales": np.random.uniform(0, 100, 100),
    "E_Sales": np.random.uniform(0, 100, 100),
    "F_Sales": np.random.uniform(0, 100, 100),
    "G_Sales": np.random.uniform(0, 100, 100),
    "A_Asset": np.random.uniform(0, 100, 100),
    "B_Asset": np.random.uniform(0, 100, 100),
    "C_Asset": np.random.uniform(0, 100, 100),
    "D_Asset": np.random.uniform(0, 100, 100),
    "E_Asset": np.random.uniform(0, 100, 100),
    "F_Asset": np.random.uniform(0, 100, 100),
    "G_Asset": np.random.uniform(0, 100, 100),
    "A_Borrow": np.random.uniform(0, 100, 100),
    "B_Borrow": np.random.uniform(0, 100, 100),
    "C_Borrow": np.random.uniform(0, 100, 100),
    "D_Borrow": np.random.uniform(0, 100, 100),
    "E_Borrow": np.random.uniform(0, 100, 100),
    "F_Borrow": np.random.uniform(0, 100, 100),
    "G_Borrow": np.random.uniform(0, 100, 100),
    "A_Shrink": np.random.uniform(0, 100, 100),
    "B_Shrink": np.random.uniform(0, 100, 100),
    "C_Shrink": np.random.uniform(0, 100, 100),
    "D_Shrink": np.random.uniform(0, 100, 100),
    "E_Shrink": np.random.uniform(0, 100, 100),
    "F_Shrink": np.random.uniform(0, 100, 100),
    "G_Shrink": np.random.uniform(0, 100, 100),
    "Sales_H_cntry_size": np.random.randint(400, 600, 100),
    "Sales_MH_cntry_size": np.random.randint(900, 1100, 100),
    "Sales_ML_cntry_size": np.random.randint(150, 250, 100),
    "Sales_L_cntry_size": np.random.randint(200, 300, 100),
    "Asset_H_cntry_size": np.random.randint(4500, 5500, 100),
    "Asset_MH_cntry_size": np.random.randint(900, 1100, 100),
    "Asset_ML_cntry_size": np.random.randint(2400, 2600, 100),
    "Asset_L_cntry_size": np.random.randint(2400, 2600, 100),
    "Borrow_H_cntry_size": np.random.randint(500, 600, 100),
    "Borrow_MH_cntry_size": np.random.randint(50, 150, 100),
    "Borrow_ML_cntry_size": np.random.randint(1900, 2100, 100),
    "Borrow_L_cntry_size": np.random.randint(1200, 1300, 100),
    "Shrink_H_cntry_size": np.random.randint(5000, 6000, 100),
    "Shrink_MH_cntry_size": np.random.randint(50000, 52000, 100),
    "Shrink_ML_cntry_size": np.random.randint(1000, 1500, 100),
    "Shrink_L_cntry_size": np.random.randint(2000, 2500, 100),
    "Sales_H_cntry_size_sector": np.random.randint(400, 600, 100),
    "Sales_MH_cntry_size_sector": np.random.randint(900, 1100, 100),
    "Sales_ML_cntry_size_sector": np.random.randint(150, 250, 100),
    "Sales_L_cntry_size_sector": np.random.randint(200, 300, 100),
    "Asset_H_cntry_size_sector": np.random.randint(4500, 5500, 100),
    "Asset_MH_cntry_size_sector": np.random.randint(900, 1100, 100),
    "Asset_ML_cntry_size_sector": np.random.randint(2400, 2600, 100),
    "Asset_L_cntry_size_sector": np.random.randint(2400, 2600, 100),
    "Borrow_H_cntry_size_sector": np.random.randint(500, 600, 100),
    "Borrow_MH_cntry_size_sector": np.random.randint(50, 150, 100),
    "Borrow_ML_cntry_size_sector": np.random.randint(1900, 2100, 100),
    "Borrow_L_cntry_size_sector": np.random.randint(1200, 1300, 100),
    "Shrink_H_cntry_size_sector": np.random.randint(5000, 6000, 100),
    "Shrink_MH_cntry_size_sector": np.random.randint(50000, 52000, 100),
    "Shrink_ML_cntry_size_sector": np.random.randint(1000, 1500, 100),
    "Shrink_L_cntry_size_sector": np.random.randint(2000, 2500, 100),
    "Sales_H_glb_size": np.random.randint(400, 600, 100),
    "Sales_MH_glb_size": np.random.randint(900, 1100, 100),
    "Sales_ML_glb_size": np.random.randint(150, 250, 100),
    "Sales_L_glb_size": np.random.randint(2000, 3000, 100),
    "Asset_H_glb_size": np.random.randint(4500, 5500, 100),
    "Asset_MH_glb_size": np.random.randint(900, 1100, 100),
    "Asset_ML_glb_size": np.random.randint(2400, 2600, 100),
    "Asset_L_glb_size": np.random.randint(2400, 2600, 100),
    "Borrow_H_glb_size": np.random.randint(500, 600, 100),
    "Borrow_MH_glb_size": np.random.randint(50, 150, 100),
    "Borrow_ML_glb_size": np.random.randint(1900, 2100, 100),
    "Borrow_L_glb_size": np.random.randint(1200, 1300, 100),
    "Shrink_H_glb_size": np.random.randint(5000, 6000, 100),
    "Shrink_MH_glb_size": np.random.randint(5000, 6000, 100),
    "Shrink_ML_glb_size": np.random.randint(1000, 1500, 100),
    "Shrink_L_glb_size": np.random.randint(200, 300, 100),
    "Sales_H_glb_size_sector": np.random.randint(400, 600, 100),
    "Sales_MH_glb_size_sector": np.random.randint(900, 1100, 100),
    "Sales_ML_glb_size_sector": np.random.randint(150, 250, 100),
    "Sales_L_glb_size_sector": np.random.randint(200, 300, 100),
    "Asset_H_glb_size_sector": np.random.randint(4500, 5500, 100),
    "Asset_MH_glb_size_sector": np.random.randint(900, 1100, 100),
    "Asset_ML_glb_size_sector": np.random.randint(2400, 2600, 100),
    "Asset_L_glb_size_sector": np.random.randint(2400, 2600, 100),
    "Borrow_H_glb_size_sector": np.random.randint(500, 600, 100),
    "Borrow_MH_glb_size_sector": np.random.randint(50, 150, 100),
    "Borrow_ML_glb_size_sector": np.random.randint(1900, 2100, 100),
    "Borrow_L_glb_size_sector": np.random.randint(1200, 1300, 100),
    "Shrink_H_glb_size_sector": np.random.randint(5000, 6000, 100),
    "Shrink_MH_glb_size_sector": np.random.randint(5000, 6000, 100),
    "Shrink_ML_glb_size_sector": np.random.randint(1000, 1500, 100),
    "Shrink_L_glb_size_sector": np.random.randint(1000, 1500, 100)
})

## Create competitor string
df["Competitors"] = [";".join(["Name" + str(j) for j in np.random.randint(1, 100, 8) if j != i]) for i in range(1,len(df) + 1)]

# Define the sectors with colors and associated industries
sectors_ndy = [
    {"name": "Technology", "color": "#D32F2F", "industries": ["Software", "Hardware", "IT Services"]},
    {"name": "Healthcare", "color": "#1976D2", "industries": ["Pharmaceuticals", "Medical Devices", "Healthcare Services"]},
    {"name": "Finance", "color": "#388E3C", "industries": ["Banking", "Insurance", "Investment Services"]},
    {"name": "Energy", "color": "#F57C00", "industries": ["Oil & Gas", "Renewable Energy", "Utilities"]},
    {"name": "Consumer Goods", "color": "#512DA8", "industries": ["Food & Beverage", "Household Products", "Apparel"]},
    {"name": "Utilities", "color": "#00796B", "industries": ["Electric", "Water", "Gas"]},
    {"name": "Real Estate", "color": "#C2185B", "industries": ["Residential", "Commercial", "Industrial"]},
    {"name": "Telecommunications", "color": "#689F38", "industries": ["Mobile", "Broadband", "Satellite"]},
    {"name": "Materials", "color": "#0288D1", "industries": ["Chemicals", "Metals & Mining", "Construction Materials"]},
    {"name": "Industrials", "color": "#7B1FA2", "industries": ["Aerospace & Defense", "Machinery", "Industrial Services"]},
    {"name": "Consumer Services", "color": "#AFB42B", "industries": ["Retail", "Travel & Leisure", "Media"]},
    {"name": "Transportation", "color": "#FBC02D", "industries": ["Airlines", "Railroads", "Logistics"]}
]

sector_to_industries = {sector["name"]: sector["industries"] for sector in sectors_ndy}

# Function to randomly select an industry based on the sector
def select_random_industry(sector):
    industries = sector_to_industries.get(sector, [])
    return random.choice(industries) if industries else None

# Apply the function to create the new 'Industry' column
df['Industry'] = df['Sector'].apply(select_random_industry)

# Sales relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df),  percentiles_sales.shape[1] - 1),
                      columns=[i+"_Sales_RC" for i in percentiles_sales.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df = pd.concat([df, rel_con2], axis=1)

# Asset relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df),  percentiles_asset.shape[1] - 1),
                      columns=[i+"_Asset_RC" for i in percentiles_asset.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df = pd.concat([df, rel_con2], axis=1)

# Borrowing relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df),  percentiles_borrow.shape[1] - 1),
                      columns=[i+"_Borrow_RC" for i in percentiles_borrow.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df = pd.concat([df, rel_con2], axis=1)

# Shrinkage relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df),  percentiles_shrink.shape[1] - 1),
                      columns=[i+"_Shrink_RC" for i in percentiles_shrink.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df = pd.concat([df, rel_con2], axis=1)

# Risk segment data
for i in ["ews" + (f"_{i}" if i else "") for i in scenario_order_risk]:
    # Randomly sample from the cateogries
    df[i] = random.choices(category_risk, k = len(df))


df["Sales_Reason"] = random.choices(["Leveraged Expansion", "Reversal", "CAPEX Investment", "Strategic Reinvestment"], k = len(df))
df["Asset_Reason"] = random.choices(["Market Gain", "Operational Expansion", "Investment Money", "Long-Term Payoff"], k = len(df))
df["Borrow_Reason"] = random.choices(["Debt History", "Size Capacity", "Liquidity Needs", "Debt Restructuring"], k = len(df))
df["Shrink_Reason"] = random.choices(["Low Profitability", "Underperformance", "Inefficiency", "Economic Crisis"], k = len(df))

############# Full Scored Dataset Large #############

# Get a list of all country codes from ISO 3166-1 using pycountry
countries = list(set([country.alpha_3 for country in pycountry.countries]) - 
     set(["ABW", "AGO", "AND", "AZE","BMU","BRB","CAF","CIV","CUB","CUW","FLK", "FJI",
         "IMN","STP","GIB","NIU","COD","IOT","ERI","KWT","GIN","GUM","NCL","GHA"])) # List of ISO Alpha-3 country codes

# Define the variables for the new dataset
sectors = ['Technology', 'Finance', 'Energy', 'Healthcare', "Consumer Goods", 'Utilities', 
           'Real Estate', 'Telecommunications', 'Materials', 'Industrials', 'Consumer Services',
           'Transportation']
sizes = ['Large', 'Medium', 'Small', 'Micro']

## Create an empty list to hold all rows
data = []
## Propensity distribution metadata
cntry_size_dist = []
cntry_size_sector_dist = []
glb_size_dist = []
glb_size_sector_dist = []

def generate_dist(suffix, cntry, size, sector = None, models = ["Sales", "Asset", "Borrow", "Shrink"]):

    out = [{"Country" : cntry, "Size" : size}]

    for i in models:
        out.append({f"{i}_{j}_{suffix}" : np.random.randint(1_000, 50_000) for j in ["H","MH","ML","L"]})

    ret = reduce(lambda a, b: {**a, **b}, out)

    if sector is not None:
        ret["Sector"] = sector

    return ret

## Populate the dataset with Sector country and size
for country in countries:
    for size in sizes:
        cntry_size_dist.append(generate_dist("cntry_size", country, size))
        for sector in sectors:
            cntry_size_sector_dist.append(generate_dist("cntry_size_sector", country, size, sector))
            for industry in sector_to_industries.get(sector, []):
                # If USA, ITA produce extra data for displaying purposes
                if country in ["USA", "ITA"]:
                    for m in range(30):
                        data.append({'Sector': sector, 'Country': country, 'Size': size, "Industry" : industry})
                
                for n, i in enumerate(range(random.randint(5,25))):
                    data.append({'Sector': sector, 'Country': country, 'Size': size, "Industry" : industry})
                    

for size in sizes:
    glb_size_dist.append(generate_dist("glb_size", "Global", size))
    for sector in sectors:
        glb_size_sector_dist.append(generate_dist("glb_size_sector", "Global", size, sector))

## Convert the list of rows into a DataFrame
df_large = pd.DataFrame(data)
cntry_size_dist_metadata = pd.DataFrame(cntry_size_dist)
cntry_size_sector_dist_metadata = pd.DataFrame(cntry_size_sector_dist)
glb_size_dist_metadata = pd.DataFrame(glb_size_dist)
glb_size_sector_dist_metadata = pd.DataFrame(glb_size_sector_dist)

## Add additional variable
df_large["Names"] = [f"Name{i}" for i in range(len(df_large))]
df_large["Sales"] = np.random.randint(0, 100_000_000, len(df_large))
df_large["Asset"] = np.random.randint(0, 100_000_000, len(df_large))

for i in ["Sales","Asset"]:
    for k in range(1,6):
        df_large[f"{i}_{k}"] = df_large[i] * np.random.uniform(0, 1, len(df_large)) 

for i in model_type_list:
    df_large[f"{i}P"] = np.random.randint(0,100, len(df_large))
    for j in percentiles_borrow.columns[1:]:
        df_large[f"{j}_{i}"] = np.random.randint(0,100, len(df_large))

## Create competitor string
df_large["Competitors"] = [";".join(["Name" + str(j) for j in np.random.randint(1, 100, 8) if j != i]) for i in range(1,len(df_large) + 1)]

# Sales relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df_large),  percentiles_sales.shape[1] - 1),
                      columns=[i+"_Sales_RC" for i in percentiles_sales.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df_large = pd.concat([df_large, rel_con2], axis=1)

# Asset relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df_large),  percentiles_asset.shape[1] - 1),
                      columns=[i+"_Asset_RC" for i in percentiles_asset.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df_large = pd.concat([df_large, rel_con2], axis=1)

# Borrowing relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df_large),  percentiles_borrow.shape[1] - 1),
                      columns=[i+"_Borrow_RC" for i in percentiles_borrow.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df_large = pd.concat([df_large, rel_con2], axis=1)

# Shrinkage relative contribution
rel_con = pd.DataFrame(np.random.rand(len(df_large),  percentiles_shrink.shape[1] - 1),
                      columns=[i+"_Shrink_RC" for i in percentiles_shrink.columns.tolist()[1:]])
rel_con2 = rel_con.div(rel_con.sum(axis=1), axis=0)
df_large = pd.concat([df_large, rel_con2], axis=1)

# Risk segment data
for i in ["ews" + (f"_{i}" if i else "") for i in scenario_order_risk]:
    # Randomly sample from the cateogries
    df_large[i] = random.choices(category_risk, k = len(df_large))


df_large["Sales_Reason"] = random.choices(["Leveraged Expansion", "Reversal", "CAPEX Investment", "Strategic Reinvestment"], k = len(df_large))
df_large["Asset_Reason"] = random.choices(["Market Gain", "Operational Expansion", "Investment Money", "Long-Term Payoff"], k = len(df_large))
df_large["Borrow_Reason"] = random.choices(["Debt History", "Size Capacity", "Liquidity Needs", "Debt Restructuring"], k = len(df_large))
df_large["Shrink_Reason"] = random.choices(["Low Profitability", "Underperformance", "Inefficiency", "Economic Crisis"], k = len(df_large))

############# Hot Zones #############

## Add Hot Zones data for Geographical Plots

# Global rates
countries = []
for country in pycountry.countries:
    countries.append({"country": country.name, "iso_alpha": country.alpha_3})
glb_rates_metadata = pd.DataFrame(countries)
glb_rates_metadata["Growth"] = np.random.rand(len(glb_rates_metadata))

# US State Rates
state_rates_metadata = pd.DataFrame({
    'state':  [state.abbr for state in us.states.STATES] + ["DC"],
    'state_name':  [state.name for state in us.states.STATES] + ["District of Columbia"],  # Full state names
    })
state_rates_metadata['Growth'] = np.random.rand(len(state_rates_metadata))

# US Counties Rates
us_counties_metadata = {
    i : 
    pd.DataFrame(
        {k["properties"]["STATE"] + k["properties"]["COUNTY"]: k["properties"]["NAME"] for k in GPlots.us_counties[j]["features"]}.items(),
        columns = ["fips","County"])
    for i,j in GPlots.fips_codes_state_code.items()
}

for _,j in us_counties_metadata.items():
    j["Growth"] = np.random.rand(len(j))

# NUTS1 Rates
cntry = []
n1 = []
for key, value_list in GPlots.region_names[1].items():
    for value in value_list:
        cntry.append(key)
        n1.append(value)

nuts1_rates_metadata = pd.DataFrame({"Country": cntry, "NUTS1": n1})
nuts1_rates_metadata["Growth"] = np.random.rand(len(nuts1_rates_metadata))

# NUTS2 Rates
cntry = []
n1 = []
n2 = []
for key, value_list in GPlots.region_names[2].items():
    for value, out in value_list.items():
        for m in out:
            cntry.append(key)  # Add the key for each value
            n1.append(value)  # Add the corresponding value
            n2.append(m)

nuts2_rates_metadata = pd.DataFrame({"Country": cntry, "NUTS1": n1, "NUTS2": n2})
nuts2_rates_metadata["Growth"] = np.random.rand(len(nuts2_rates_metadata))

# NUTS3 Rates
cntry = []
n1 = []
n2 = []
n3 = []
for key, value_list in GPlots.region_names[3].items():
    for value, out in value_list.items():
        for m, out2 in out.items():
            for o in out2:
                cntry.append(key)  # Add the key for each value
                n1.append(value)  # Add the corresponding value
                n2.append(m)
                n3.append(o)

nuts3_rates_metadata = pd.DataFrame({"Country": cntry, "NUTS1": n1, "NUTS2": n2, "NUTS3": n3})
nuts3_rates_metadata["Growth"] = np.random.rand(len(nuts3_rates_metadata))

################ FORMATTING APP COMPONENTS ################

APP_BACKGROUND_COLOR = '#f8f8f8'
BACKGROUND_COLOR = '#e8f4f8'

# Define category colors
category_colors = {
    'Green': '#0046BF',
    'Yellow': '#669EFF',
    'Red': '#CCDFFF',
    'Orange': '#99BFFF',
    'Selected': '#000000'  # Black for selected state
}

# Generic color button style
COLOR_BUTTON_STYLE = {
    'width': '25px', 
    'height': '25px', 
    'lineHeight': '25px',
    'borderRadius': '50%', 
    'border': 'none', 
    'margin': '10px',
    'boxShadow': 'inset 0px 4px 6px rgba(0, 0, 0, 0.3)'
}

# Generic name bubble style
NAME_BUBBLE_STYLE = {
    'borderRadius': '50%',
    'width': '100px',
    'height': '100px',
    'lineHeight': '100px',
    'textAlign': 'center',
    'margin': '10px',
    'display': 'inline-block',
    'cursor': 'pointer',
    'fontSize': '16px',
    'transition': '0.3s',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
}

CARD_STYLE = {
    'background-color': BACKGROUND_COLOR, 
    'padding': '20px', 
    'box-shadow': '2px 2px 5px rgba(0,0,0,0.1)', 
    'border-radius': '10px', 
    'flex': 1, 
    'margin': '10px', 
    'position': 'relative'
}

MODEL_BUTTON_STYLE = {
    'justifyContent': 'center',  # Center horizontally
    'alignItems': 'center',  # Center vertically
    'margin': '20px auto',  # Center the button block itself
    'padding': '10px 20px',  # Remove extra padding
    'fontSize': '16px',
    'fontWeight': 'bold',
    'backgroundColor': '#cccccc',
    'color': 'black',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
    'height': '50px',  # Set a fixed height for the button
}

# Preset the "Okay" button style for reuse
OKAY_BUTTON_STYLE = {
    'display': 'none',  # Initially hidden
    'justifyContent': 'center',  # Center horizontally
    'alignItems': 'center',  # Center vertically
    'margin': '20px auto',  # Center the button block itself
    'padding': '10px 20px',  # Remove extra padding
    'fontSize': '16px',
    'fontWeight': 'bold',
    'color': '#fff',
    'backgroundColor': '#007BFF',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
    'height': '50px',  # Set a fixed height for the button
}

# Preset the grid container style for reuse
SECTOR_CONTAINER_STYLE = {
    'display': 'none',  # Hidden by default
    'gridTemplateColumns': 'repeat(4, 1fr)',
    'gridTemplateRows': 'repeat(3, 1fr)',
    'gap': '10px',
    'justifyItems': 'center',
    'alignItems': 'center',
    'width': '500px',
    'height': 'auto',  # Allow the container to auto-adjust its height
    'border': '2px solid black',
    'borderRadius': '20px',
    'padding': '10px',
    'boxShadow': '0px 10px 15px rgba(0, 0, 0, 0.2)',
    'backgroundColor': '#f9f9f9',
    'margin': '50px auto',
    'marginTop': '100px'  # Set top margin to 100px
}

# Preset sector/industry grid style for reuse
TILE_STYLE = {
    'display': 'flex',
    'justifyContent': 'center',
    'alignItems': 'center',
    'border': '2px solid #fff',
    'borderRadius': '15px',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
    'fontSize': '14px', 
    'cursor': 'pointer',
    'backgroundColor': '#000000',
    'color': '#fff',
    'textAlign': 'center',
    'fontWeight': 'bold',
    'width': '100px',
    'height': '100px',
    'padding': '5px',
    'textOverflow': 'ellipsis',
    'wordWrap': 'break-word',
    'overflow': 'hidden',
    'transition': 'transform 0.2s, box-shadow 0.2s'
}

# Displayed text styling
display_text_style = {
    "geography": {'color': '#555', 'fontWeight': 'bold', 'marginBottom': '10px'},
    "sector": {'color': '#28a745', 'marginBottom': '10px'},
    "industry": {'color': '#007bff', 'marginBottom': '10px'}
}

# Define styles for the boxes with a new neutral yet vibrant palette
BOX_STYLE = {
    'width': '140px',
    'height': '140px',
    'display': 'inline-block',
    'textAlign': 'center',
    'lineHeight': '140px',
    'margin': '10px',
    'border': '2px solid #aaa',
    'borderRadius': '12px',
    'cursor': 'pointer',
    'fontWeight': 'bold',
    'fontSize': '22px',  # Larger text for better readability
    'color': '#333',
    'transition': 'all 0.3s ease',
    'backgroundColor': '#f4f4f4',
    'boxShadow': '1px 1px 5px rgba(0,0,0,0.1)'
}

# Improved vibrant yet neutral color palette
BOX_STYLE_FULL = {
    'large': {**BOX_STYLE, 'backgroundColor': '#AEC6CF'},  # Soft cyan
    'medium': {**BOX_STYLE, 'backgroundColor': '#FFB347'},  # Warm orange
    'small': {**BOX_STYLE, 'backgroundColor': '#B39EB5'},  # Muted lavender
    'micro': {**BOX_STYLE, 'backgroundColor': '#FDFD96'}   # Light pastel yellow
}

# Hover style for boxes
HOVER_STYLE = {
    'transform': 'scale(1.05)',
    'boxShadow': '3px 3px 8px rgba(0,0,0,0.15)'
}

# Print page style
PRINT_STYLE = {
    'width': '460px', 
    'height': 'auto', 
    'border': '2px solid black', 
    'borderRadius': '10px',
    'padding': '10px', 
    'margin': '20px auto',
    'textAlign': 'center',
    'fontSize': '20px',
    'fontWeight': 'bold',
    'backgroundColor': '#f8f9fa',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
    'fontFamily': 'sans-serif',
}

# Output container styling
out_text_style = {
    "geography": {'color': '#555', 'fontWeight': 'bold', 'marginBottom': '10px'},
    "sector": {'color': '#28a745', 'marginBottom': '10px'},
    "industry": {'color': '#007bff', 'marginBottom': '10px'},
    "size": {'color': 'maroon', 'marginBottom': '10px'}
}

## Next button style
NEXT_BUTTON_STYLE = {
            'width': '60px',
            'height': '60px',
            'fontSize': '30px',
            'color': 'white',
            'backgroundColor': '#333',  # Dark grey button
            'border': 'none',
            'borderRadius': '50%',  # Make it circular
            'cursor': 'pointer',
            'boxShadow': '0px 8px 12px rgba(0, 0, 0, 0.3)',  # Subtle shadow for depth
            'transition': 'all 0.3s ease',
            'fontWeight': 'bold',
            'display': 'flex',  # Flexbox to center the content
            'justifyContent': 'center',  # Horizontally center
            'alignItems': 'center',  # Vertically center
            'lineHeight': 'normal',  # Fix alignment issues with symbols
            'textAlign': 'center',
            'marginLeft': '20px',  # Positioned on the left side
            'fontFamily': 'Arial, sans-serif',  # Clean font family
        }

# Segment label style
SEGMENT_LABEL = {
    'fontSize': '30px',  # Large font size for emphasis
    'color': '#FFFFFF',  # Text color (white)
    'background': '#4682B4',
    'padding': '10px 20px',  # Padding around the label
    'borderRadius': '50px 15px 50px 15px',  # Creative rounded corners for shape
    'boxShadow': '0px 10px 25px rgba(0, 0, 0, 0.5)',  # Drop shadow for depth
    'textAlign': 'center',  # Center-align the text
    # 'width': '350px',  # Width of the container
    'margin': '10px',  # Small margin around the container
    'fontWeight': 'bold',  # Bold text for emphasis
    'fontFamily': 'Verdana, sans-serif',  # Clean and modern font
    'border': '3px solid #FFFFFF',  # White border for pop effect
    'transform': 'rotate(2deg)',  # Slight rotation for dynamic feel
}

# Define app covrage of full page
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;  /* Ensure the body and html take up full viewport height */
            }
            #app-container {
                height: 100vh;  /* Make the app container take up the full viewport height */
                display: flex;
                flex-direction: column;
            }
        </style>
    </head>
    <body>
        <div id="app-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def model_type_prep(df, model):

    df = df.sort_values(model + "P", ascending = False)

    bins = [0, 25, 50, 75, 100]
    labels = ['Red', 'Orange', 'Yellow', 'Green']

    # Use pd.cut() to map the values
    df['Category'] = pd.cut(df[model + "P"], bins=bins, labels=labels, right=False, include_lowest=True)

    return df    