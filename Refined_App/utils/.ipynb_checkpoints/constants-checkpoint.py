## Define color dictionary used by the app
COLORS = {
    "background" : "white",
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
    "exploratory_text" : "2.5em",
    "targeted_text" : "2.5em",
}

## Define Background color
APP_BACKGROUND_COLOR = "white"

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
SECTORS = [
    "All",
    "Technology",
    "Healthcare",
    "Finance",
    "Energy",
    "Utilities",
    "Real Estate",
    "Consumer Goods",
    "Telecommunications",
    "Materials",
    "Industrials",
    "Consumer Services",
    "Transportation"
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
    "T" : "0B1164",
    "F" : "white"
}

## Early Warning Colors
EWS_COLOR = {
    "L":"9ADD84",
    "M":"F8DA6E",
    "H":"EE833A",
    "S":"E2556A"
}




