import dash
from dash import html

## Define path
PATH = ""

## Define color dictionary used by the app
COLORS = {
    "background" : "white",
    "demo_block" : "black", # Azure Radiance Blue
    "details_block" : "white", # Azure Radiance Blue
    "demo_text" : "white",
    "details_text" : "black",
    "exploratory_block" : "#007BFF", # Azure Radiance Blue
    "targeted_block" : "#28A745", # Eucalyptus Green
    "exploratory_text" : "white",
    "targeted_text" : "white",
}

## Define Fonts
FONTS = {
    "headings" : "Georgia",
    "headings-fallback" : "sans-serif", # Generic fallbacks in case desired font is unavailable
    "sub-headings" : "Merriweather",
    "sub-headings-fallback" : "serif",
    "body" : "Crimson Text",
    "body-fallback" : "sans-serif",
    "all-caps-heading" : "Trajan Pro",
    "all-caps-heading-fallback" : "sans-serif",
}

## Define font sizes
FONT_SIZES = {
    "demo_text" : "3em",
    "details_text" : "3em",
    "exploratory_text" : "2.5em",
    "targeted_text" : "2.5em",
}

## Define Background color
APP_BACKGROUND_COLOR = "white"

## Heatmap colors
HEATMAP_GEO = {
    "hot-zones" : "Thermal",
    "risk-segments" : "RdYlGn_r"
}

## Define metadata column names
METADATA_COLUMNS = {
    "GROWTH_RATE_COLUMN" : "Growth_Rate",
    "COUNTRY_COLUMN" : "Country",
    "STATE_COLUMN" : "State",
    "STATE_NAME_COLUMN" : "States_Full",
    "COUNTY_COLUMN" : "COUNTY_ID",
    "COUNTY_NAME_COLUMN" : "COUNTY_NAME",
    "NUTS_NAME_COLUMN" : "NUTS_NAME",
    "NUTS1_FILTER" : "Country",
    "NUTS2_FILTER" : "NUTS1_ID",
    "NUTS3_FILTER" : "NUTS2_ID",
    "NUTS1_LOCATION" : "NUTS1_ID",
    "NUTS2_LOCATION" : "NUTS2_ID",
    "NUTS3_LOCATION" : "NUTS3_ID",
    "TREE_PARENT" : "parent",
    "TREE_CHILD" : "child",
    "TREE_COUNT" : "Count",
    "TREE_TYPE" : "Type",
}

## Sector Names
SECTORS = ["HiTech", "Agriculture", "Transportation", "Consumer_Products", "Unassigned", "Communication", "Trade", "Business_Services", "Business_Products", "Construction", "Services", "Mining", "Health_Care", "EnergyExpL_Prod", "Utilities"]

SECTORS_ALL = ["All", "HiTech", "Agriculture", "Transportation", "Consumer_Products", "Unassigned", "Communication", "Trade", "Business_Services", "Business_Products", "Construction", "Services", "Mining", "Health_Care", "EnergyExpL_Prod", "Utilities"]

## Covered countries
COVERED_COUNTRIES = [
    "ALB", "AUS", "AUT", "BEL", "BGR", "COL", "ESP", "FIN", "FRA", "HUN", "ITA", "KOR", "MDA", "NZL", "POL", "PRT", "ROU", "RUS", "SRB", "SVK", "SWE", "THA", "UKR", "USA", "VNM", "DEU", "DNK", "GBR", "IDN", "ISL", "JPN", "LVA", "MEX", "MYS", "PHL", "SVN", "ZAF", "CAN", "CHE", "CZE", "DZA", "EST", "HRV", "ISR", "LTU", "SGP", "TWN", "MKD", "NOR", "BIH", "LUX", "NLD", "PAK", "GRC", "KAZ", "MNE", "BRA", "IND", "TUR", "IRN", "MAR", "HKG", "MLT"
]

## Risk Score Type
RISK_SCORES = [
    "Overall Risk",
    "Macro Risk", "Business Risk", "Financial Risk",
    "Social Risk", "Political Risk", "Security Risk"
]

## NUTS Countries
NUTS_COUNTRIES = [
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

## Tree Map Color palette
TREE_CMAP = "Balance"

## Selected Table Name
SELECTED_TABLE_HEADER = "Selected Portfolio"

## Propensity Colors
PROPENSITY_COLOR = {
    "T" : "#0B1164",
    "F" : "White"
}

## Early Warning Colors
EWS_COLOR = {
    "L":"#9ADD84",
    "M":"#F8DA6E",
    "H":"#EE833A",
    "S":"#E2556A"
}

## Details Grid
NUM_ROWS = 3
NUM_COLS = 4
TOTAL_CELLS = NUM_ROWS * NUM_COLS

## Grid Cells
GRID_CELLS = ["Model Introduction", "Top-Growth Milestones"]
## Define what each grid contains i.e. populated or empty
GRID_CELLS = GRID_CELLS + ["Coming Soon"]*(TOTAL_CELLS - len(GRID_CELLS))

## Grid Cell Content
GRID_CONTENT = {
    "G1" : html.Video(
        controls = True,
        src = f"assets/OppAnalytics_v1.mp4",
        style = {"width":"100%"}
    ),
    "G2" : html.Div("Content Test", style={"textAlign": "center"})
}

GRID_CONTENT = {
    **GRID_CONTENT,
    **{
        f"G{i}" : html.Div("Coming Soon Content", style={"textAlign": "center"}) for i in range(len(GRID_CONTENT)+2, TOTAL_CELLS+1)
    }
}