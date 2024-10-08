import numpy as np
import pandas as pd
import requests
import pycountry
import plotly.express as px
import plotly.graph_objects as go
import us
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Geo data for NUTS1,2,3
filtered_features = {
    1 : json.load(open("filtered_features_nuts1.json")),
    2 : json.load(open("filtered_features_nuts2.json")),
    3 : json.load(open("filtered_features_nuts3.json"))
}
region_names = {
    1 : json.load(open("region_names_nuts1.json")),
    2 : json.load(open("region_names_nuts2.json")),
    3 : json.load(open("region_names_nuts3.json"))
}
region_ids = {
    1 : json.load(open("region_ids_nuts1.json")),
    2 : json.load(open("region_ids_nuts2.json")),
    3 : json.load(open("region_ids_nuts3.json"))
}

nuts_name_map = json.load(open("nuts_name_map.json"))

nuts1_names = [item for sublist in region_names[1].values() for item in sublist]
nuts2_names = [item for sublist in region_names[2].values() for item in sublist]
nuts3_names = [item for sublist in region_names[3].values() for item in sublist]

nuts_countries = [i for i,j in region_names[1].items() if len(j) > 0]
nuts_countries_add = [pycountry.countries.lookup(i).alpha_3 for i in nuts_countries]
nuts_countries += nuts_countries_add

# US Counties
us_counties = json.load(open("counties_out.json"))

custom_color_scale = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173", "#5254a3", "#8ca252", "#bd9e39", "#ad494a", "#a55194",
    "#6b6ecf", "#b5cf6b", "#e7ba52", "#d6616b", "#ce6dbd", "#9c9ede", "#cedb9c", "#e7cb94", "#e7969c", "#de9ed6",
    "#17becf", "#9edae5",
    "#ff6347", "#4682b4", "#daa520", "#b22222", "#32cd32", "#8b4513", "#ff69b4", "#cd5c5c", "#6495ed", "#ff4500",
    "#7fffd4", "#b0c4de", "#ff00ff", "#808000", "#e9967a", "#8a2be2", "#ff1493", "#1e90ff", "#bdb76b", "#f08080",
    "#3cb371", "#da70d6", "#c71585", "#40e0d0", "#ff6347", "#4682b4", "#daa520", "#b22222", "#32cd32", "#8b4513",
    "#ff69b4", "#cd5c5c", "#6495ed", "#ff4500", "#7fffd4", "#b0c4de", "#ff00ff", "#808000", "#e9967a", "#8a2be2",
    "#ff1493", "#1e90ff", "#bdb76b", "#f08080", "#3cb371", "#da70d6", "#c71585", "#40e0d0"
]

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


flag_colors = {
    "AFG": "#000000",  # Afghanistan - Black
    "ALB": "#e41e26",  # Albania - Red
    "DZA": "#006233",  # Algeria - Green
    "AND": "#ffce00",  # Andorra - Yellow
    "AGO": "#ce1126",  # Angola - Red
    "ARG": "#74acdf",  # Argentina - Light blue
    "ARM": "#d90012",  # Armenia - Red
    "AUS": "#00008b",  # Australia - Dark blue
    "AUT": "#ed2939",  # Austria - Red
    "AZE": "#009639",  # Azerbaijan - Green
    "BHR": "#ce1126",  # Bahrain - Red
    "BGD": "#006a4e",  # Bangladesh - Green
    "BLR": "#d22730",  # Belarus - Red
    "BEL": "#ffd100",  # Belgium - Yellow
    "BLZ": "#0033a0",  # Belize - Blue
    "BEN": "#008751",  # Benin - Green
    "BTN": "#ffcc00",  # Bhutan - Yellow
    "BOL": "#ffd700",  # Bolivia - Yellow
    "BIH": "#002395",  # Bosnia and Herzegovina - Blue
    "BWA": "#00a2e8",  # Botswana - Blue
    "BRA": "#009739",  # Brazil - Green
    "BRN": "#ffcc00",  # Brunei - Yellow
    "BGR": "#00966e",  # Bulgaria - Green
    "BFA": "#009e49",  # Burkina Faso - Green
    "BDI": "#ff0000",  # Burundi - Red
    "CPV": "#003893",  # Cape Verde - Blue
    "KHM": "#032ea1",  # Cambodia - Blue
    "CMR": "#007a5e",  # Cameroon - Green
    "CAN": "#ff0000",  # Canada - Red
    "CAF": "#0072c6",  # Central African Republic - Blue
    "TCD": "#00209f",  # Chad - Blue
    "CHL": "#0033a0",  # Chile - Blue
    "CHN": "#de2910",  # China - Red
    "COL": "#ffd700",  # Colombia - Yellow
    "COM": "#3a75c4",  # Comoros - Blue
    "COD": "#007fff",  # Congo (DRC) - Blue
    "COG": "#009e49",  # Congo (Republic) - Green
    "CRI": "#002b7f",  # Costa Rica - Blue
    "CIV": "#009e60",  # Côte d'Ivoire - Green
    "HRV": "#f40609",  # Croatia - Red
    "CUB": "#002a8f",  # Cuba - Blue
    "CYP": "#d4a017",  # Cyprus - Yellow
    "CZE": "#d7141a",  # Czech Republic - Red
    "DNK": "#c60c30",  # Denmark - Red
    "DJI": "#0c5eaf",  # Djibouti - Blue
    "DMA": "#008000",  # Dominica - Green
    "DOM": "#00247d",  # Dominican Republic - Blue
    "ECU": "#ffdf00",  # Ecuador - Yellow
    "EGY": "#ce1126",  # Egypt - Red
    "SLV": "#0038a8",  # El Salvador - Blue
    "GNQ": "#3e9a00",  # Equatorial Guinea - Green
    "ERI": "#3a9d23",  # Eritrea - Green
    "EST": "#0072ce",  # Estonia - Blue
    "ETH": "#089b3b",  # Ethiopia - Green
    "FJI": "#009eeb",  # Fiji - Blue
    "FIN": "#003580",  # Finland - Blue
    "FRA": "#0055a4",  # France - Blue
    "GAB": "#009639",  # Gabon - Green
    "GMB": "#3e5eb9",  # Gambia - Blue
    "GEO": "#f2a800",  # Georgia - Yellow
    "DEU": "#ffce00",  # Germany - Yellow
    "GHA": "#fcd116",  # Ghana - Yellow
    "GRC": "#0d5eaf",  # Greece - Blue
    "GRD": "#007a5e",  # Grenada - Green
    "GTM": "#4997d0",  # Guatemala - Blue
    "GIN": "#ce1126",  # Guinea - Red
    "GNB": "#ce1126",  # Guinea-Bissau - Red
    "GUY": "#009739",  # Guyana - Green
    "HTI": "#00209f",  # Haiti - Blue
    "HND": "#0073cf",  # Honduras - Blue
    "HUN": "#2a8d45",  # Hungary - Green
    "ISL": "#003897",  # Iceland - Blue
    "IND": "#ff9933",  # India - Orange
    "IDN": "#d01c1f",  # Indonesia - Red
    "IRN": "#da0000",  # Iran - Red
    "IRQ": "#ce1126",  # Iraq - Red
    "IRL": "#009a44",  # Ireland - Green
    "ISR": "#0038a8",  # Israel - Blue
    "ITA": "#008c45",  # Italy - Green
    "JAM": "#ffb916",  # Jamaica - Yellow
    "JPN": "#bc002d",  # Japan - Red
    "JOR": "#007a33",  # Jordan - Green
    "KAZ": "#0078c8",  # Kazakhstan - Blue
    "KEN": "#006341",  # Kenya - Green
    "KIR": "#0083b7",  # Kiribati - Blue
    "PRK": "#ed1c27",  # North Korea - Red
    "KOR": "#003478",  # South Korea - Blue
    "KWT": "#007a3d",  # Kuwait - Green
    "KGZ": "#d31e2b",  # Kyrgyzstan - Red
    "LAO": "#002868",  # Laos - Blue
    "LVA": "#9e3039",  # Latvia - Red
    "LBN": "#cd202c",  # Lebanon - Red
    "LSO": "#00209f",  # Lesotho - Blue
    "LBR": "#bf0a30",  # Liberia - Red
    "LBY": "#239e46",  # Libya - Green
    "LIE": "#00247d",  # Liechtenstein - Blue
    "LTU": "#ffb915",  # Lithuania - Yellow
    "LUX": "#9b1b30",  # Luxembourg - Red
    "MDG": "#007e3a",  # Madagascar - Green
    "MWI": "#ff0000",  # Malawi - Red
    "MYS": "#010066",  # Malaysia - Blue
    "MDV": "#007e3a",  # Maldives - Green
    "MLI": "#14b53a",  # Mali - Green
    "MLT": "#e00000",  # Malta - Red
    "MHL": "#0033a0",  # Marshall Islands - Blue
    "MRT": "#009739",  # Mauritania - Green
    "MUS": "#ef4135",  # Mauritius - Red
    "MEX": "#006847",  # Mexico - Green
    "FSM": "#009de0",  # Micronesia - Blue
    "MDA": "#0033a0",  # Moldova - Blue
    "MCO": "#ce1126",  # Monaco - Red
    "MNG": "#c4272f",  # Mongolia - Red
    "MNE": "#c8102e",  # Montenegro - Red
    "MAR": "#c1272d",  # Morocco - Red
    "MOZ": "#009639",  # Mozambique - Green
    "MMR": "#fed100",  # Myanmar - Yellow
    "NAM": "#003893",  # Namibia - Blue
    "NRU": "#002b7f",  # Nauru - Blue
    "NPL": "#dc143c",  # Nepal - Red
    "NLD": "#21468b",  # Netherlands - Blue
    "NZL": "#00247d",  # New Zealand - Blue
    "NIC": "#003893",  # Nicaragua - Blue
    "NER": "#ffa500",  # Niger - Orange
    "NGA": "#008751",  # Nigeria - Green
    "MKD": "#d20000",  # North Macedonia - Red
    "NOR": "#ba0c2f",  # Norway - Red
    "OMN": "#d81a22",  # Oman - Red
    "PAK": "#01411c",  # Pakistan - Green
    "PLW": "#0099cc",  # Palau - Blue
    "PAN": "#005aa7",  # Panama - Blue
    "PNG": "#000000",  # Papua New Guinea - Black
    "PRY": "#0038a8",  # Paraguay - Blue
    "PER": "#d91023",  # Peru - Red
    "PHL": "#0038a8",  # Philippines - Blue
    "POL": "#dc143c",  # Poland - Red
    "PRT": "#006847",  # Portugal - Green
    "QAT": "#8d1b3d",  # Qatar - Maroon
    "ROU": "#002b7f",  # Romania - Blue
    "RUS": "#d52b1e",  # Russia - Red
    "RWA": "#fad201",  # Rwanda - Yellow
    "KNA": "#00a74d",  # Saint Kitts and Nevis - Green
    "LCA": "#002366",  # Saint Lucia - Blue
    "VCT": "#009739",  # Saint Vincent and the Grenadines - Green
    "WSM": "#ce1126",  # Samoa - Red
    "SMR": "#4c92c3",  # San Marino - Blue
    "STP": "#12ad2b",  # Sao Tome and Principe - Green
    "SAU": "#006c35",  # Saudi Arabia - Green
    "SEN": "#00853f",  # Senegal - Green
    "SRB": "#c6363c",  # Serbia - Red
    "SYC": "#003da5",  # Seychelles - Blue
    "SLE": "#1eb53a",  # Sierra Leone - Green
    "SGP": "#ef3340",  # Singapore - Red
    "SVK": "#0b4ea2",  # Slovakia - Blue
    "SVN": "#0056a0",  # Slovenia - Blue
    "SLB": "#007847",  # Solomon Islands - Green
    "SOM": "#4189dd",  # Somalia - Blue
    "ZAF": "#00853f",  # South Africa - Green
    "SSD": "#078930",  # South Sudan - Green
    "ESP": "#aa151b",  # Spain - Red
    "LKA": "#8d2029",  # Sri Lanka - Maroon
    "SDN": "#007a3d",  # Sudan - Green
    "SUR": "#377e3f",  # Suriname - Green
    "SWE": "#004b87",  # Sweden - Blue
    "CHE": "#d52b1e",  # Switzerland - Red
    "SYR": "#ce1126",  # Syria - Red
    "TWN": "#00247d",  # Taiwan - Blue
    "TJK": "#006847",  # Tajikistan - Green
    "TZA": "#00a859",  # Tanzania - Green
    "THA": "#ed1c24",  # Thailand - Red
    "TLS": "#0000ff",  # Timor-Leste - Blue
    "TGO": "#006a4e",  # Togo - Green
    "TON": "#c8102e",  # Tonga - Red
    "TTO": "#e00000",  # Trinidad and Tobago - Red
    "TUN": "#e70013",  # Tunisia - Red
    "TUR": "#e30a17",  # Turkey - Red
    "TKM": "#009a44",  # Turkmenistan - Green
    "TUV": "#00a1e4",  # Tuvalu - Blue
    "UGA": "#ffce00",  # Uganda - Yellow
    "UKR": "#005bbb",  # Ukraine - Blue
    "ARE": "#00732f",  # United Arab Emirates - Green
    "GBR": "#00247d",  # United Kingdom - Blue
    "USA": "#b22234",  # United States - Red
    "URY": "#0038a8",  # Uruguay - Blue
    "UZB": "#3eb489",  # Uzbekistan - Green
    "VUT": "#000000",  # Vanuatu - Black
    "VEN": "#ffe600",  # Venezuela - Yellow
    "VNM": "#da251d",  # Vietnam - Red
    "YEM": "#ce1126",  # Yemen - Red
    "ZMB": "#ff8100",  # Zambia - Orange
    "ZWE": "#009739"  # Zimbabwe - Green
}

# Retrieve Counties geo data
def fetch_counties_geojson():

    ## Get counties geojson
    r = requests.get('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
    counties = json.loads(r.text)

    ## Convert data into dict form
    ret = {i: {'type': 'FeatureCollection',
               'features': [f for f in counties['features'] if f['properties']['STATE'] == i]
               }
           for i in fips_codes_state_code.values()
           }

    return ret

## Retrieve NUTS data
def fetch_nuts1_geojson():
    """
    Fetches the NUTS1 regions GeoJSON for Europe from an online resource.
    """
    # URL to the NUTS1 regions GeoJSON
    url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_4326_LEVL_1.geojson"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve NUTS1 GeoJSON data")
        return None

def fetch_nuts2_geojson():
    """
    Fetches the NUTS2 regions GeoJSON for Europe from an online resource.
    """
    # URL to the NUTS2 regions GeoJSON
    url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_4326_LEVL_2.geojson"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve NUTS2 GeoJSON data")
        return None

def fetch_nuts3_geojson():
    """
    Fetches the NUTS3 regions GeoJSON for Europe from an online resource.
    """
    # URL to the NUTS2 regions GeoJSON
    url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_4326_LEVL_3.geojson"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve NUTS3 GeoJSON data")
        return None

## Exclude far away territories
def exclude_islands_or_territories(features, country_code):
    """
    Excludes islands or territories based on country and specific NUTS codes.
    """
    # Define the NUTS codes or conditions to exclude specific regions
    exclusion_list = {
        "FR": ["FRY", "FRO"],  # Exclude French overseas territories
        "ES": ["ES7"],         # Exclude Canary Islands for Spain
        # Add more exclusions here for other countries as needed
    }

    if country_code in exclusion_list:
        return [feature for feature in features if not feature["properties"]["NUTS_ID"].startswith(tuple(exclusion_list[country_code]))]
    return features

def convert_to_iso2(country_identifier):
    # First, try to match the identifier as a country name
    try:
        country = pycountry.countries.get(name=country_identifier)
        if country:
            return country.alpha_2
    except LookupError:
        pass
    
    # Next, try to match as a 3-digit ISO code
    try:
        country = pycountry.countries.get(alpha_3=country_identifier)
        if country:
            return country.alpha_2
    except LookupError:
        pass
    
    # Finally, check if it's already a 2-digit ISO code
    try:
        country = pycountry.countries.get(alpha_2=country_identifier)
        if country:
            return country.alpha_2
    except LookupError:
        pass
    
    # If no match is found, return None or raise an exception
    return None

def plot_nuts_country(country_name, nuts = 1, nuts1 = None, nuts2 = None, background_color = "white"):
    
    # Match the country name to the ISO alpha-2 code using pycountry
    try:
        country_code = pycountry.countries.lookup(country_name).alpha_2
    except LookupError:
        print(f"Could not find country: {country_name}")
        return

    if not filtered_features[nuts] or len(filtered_features[nuts]) == 0:
        print(f"No NUTS1 data available for the country: {country_name}")
        return

    # Create a GeoJSON object with the filtered features
    country_geojson = {
        "type": "FeatureCollection"
    }
    if nuts == 1:
        country_geojson["features"] = filtered_features[nuts][country_code]
        names = region_names[nuts][country_code]
    elif nuts == 2:
        nuts1 = nuts_name_map["1"][nuts1]
        country_geojson["features"] = [j for i,j in filtered_features[nuts][country_code][nuts1].items()]
        names = region_names[nuts][country_code][nuts1]
    else:
        nuts1 = nuts_name_map["1"][nuts1]
        nuts2 = nuts_name_map["2"][nuts2]
        country_geojson["features"] = [j for i,j in filtered_features[nuts][country_code][nuts1][nuts2].items()]
        names = region_names[nuts][country_code][nuts1][nuts2]

    # Create a choropleth map with the NUTS1 regions outlined
    fig = px.choropleth(
        geojson=country_geojson,
        locations=names,
        color=names,  # Color by NUTS region IDs
        featureidkey="properties.NAME_LATN",
        projection="mercator",
        title = "",
        color_discrete_sequence=custom_color_scale,  # Use the custom 50-color discrete scale
    )
    
    fig.update_traces(
            hovertemplate="<b>%{location}</b><extra></extra>",
        )
    
    # Update the layout to focus on the country and increase the plot size
    fig.update_geos(
        visible=False,
        fitbounds="geojson",
        bgcolor=background_color
    )

    # Increase plot size and remove padding
    fig.update_layout(
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    fig.update_traces(showlegend=False)
    
    return fig


def plot_nuts_country_hotzones(country_name, input_df, nuts = 1, nuts1 = None, nuts2 = None, background_color = "white"):
    
    # Match the country name to the ISO alpha-2 code using pycountry
    try:
        country_code = pycountry.countries.lookup(country_name).alpha_2
    except LookupError:
        print(f"Could not find country: {country_name}")
        return

    if not filtered_features[nuts] or len(filtered_features[nuts]) == 0:
        print(f"No NUTS1 data available for the country: {country_name}")
        return

    # Create a GeoJSON object with the filtered features
    country_geojson = {
        "type": "FeatureCollection"
    }
    if nuts == 1:
        country_geojson["features"] = filtered_features[nuts][country_code]
        names = region_names[nuts][country_code]
        sub = input_df[input_df["Country"] == country_code]
        sub = sub.set_index('NUTS1').loc[names].reset_index()
    elif nuts == 2:
        nuts1 = nuts_name_map["1"][nuts1]
        print(nuts1)
        country_geojson["features"] = [j for i,j in filtered_features[nuts][country_code][nuts1].items()]
        names = region_names[nuts][country_code][nuts1]
        sub = input_df[(input_df["Country"] == country_code) & (input_df["NUTS1"] == nuts1)]
        sub = sub.set_index('NUTS2').loc[names].reset_index()
    else:
        nuts1 = nuts_name_map["1"][nuts1]
        nuts2 = nuts_name_map["2"][nuts2]
        country_geojson["features"] = [j for i,j in filtered_features[nuts][country_code][nuts1][nuts2].items()]
        names = region_names[nuts][country_code][nuts1][nuts2]
        sub = input_df[(input_df["Country"] == country_code) & (input_df["NUTS1"] == nuts1) & (input_df["NUTS2"] == nuts2)]
        sub = sub.set_index('NUTS3').loc[names].reset_index()

    # Create a choropleth map with the NUTS1 regions outlined
    fig = px.choropleth(
        geojson=country_geojson,
        locations=names,
        color=sub["Growth"]*100,  # Color by NUTS region IDs
        featureidkey="properties.NAME_LATN",
        projection="mercator",
        title = "",
        color_continuous_scale="Thermal",  # Use the custom 50-color discrete scale
    )
    
    fig.update_traces(
            hovertemplate="<b>%{location}</b><br>Growth: %{z:.2f}%<extra></extra>",
        )
    
    # Update the layout to focus on the country and increase the plot size
    fig.update_geos(
        visible=False,
        fitbounds="geojson",
        bgcolor=background_color
    )

    # Increase plot size and remove padding
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Growth<br>Propensity", # Remove the title from the color bar
            titleside="top",
            tickvals=[],            # Remove tick values (i.e., labels)
            ticks='',               # Disable tick marks
            showticklabels=False    # Do not show tick labels
        ),
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=10, r=10, t=10, b=10),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    fig.update_traces(showlegend=False)
    
    return fig

def plot_global_country(background_color = "white"):

    # Use pycountry to get all countries with their ISO alpha-3 codes
    countries = []
    for country in pycountry.countries:
        countries.append({"country": country.name, "iso_alpha": country.alpha_3})

    # Convert the list of dictionaries into a pandas DataFrame
    world_data = pd.DataFrame(countries)

    # Assign colors from the flag color dictionary to each country based on ISO code
    color_map = {row['iso_alpha']: flag_colors.get(row['iso_alpha'], '#cccccc') for index, row in world_data.iterrows()}

    # Create figure
    fig = px.choropleth(
        world_data,
            locations="iso_alpha",
            color="iso_alpha",
            hover_name="iso_alpha",  # Set hover to show only the ISO code
            projection="natural earth",
            title="",
            color_discrete_map=color_map  # Use the flag colors
        ).update_traces(hovertemplate='%{hovertext}<extra></extra>',
                       showlegend=False)  # Customize hover template to show only ISO code

    fig.update_geos(
    lakecolor="lightblue",  # Color of lakes
    projection_type="natural earth",
    showlakes=True,  # Ensure that lakes are shown and colored
    bgcolor=background_color
    )

    # Increase plot size and remove padding
    fig.update_layout(
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    return fig


def plot_global_country_hotzones(df, background_color = "white"):

    df["Growth"] = df["Growth"]*100
    
    # Create figure
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="Growth",
        hover_name="iso_alpha",  # Set hover to show only the ISO code
        projection="natural earth",
        title="",
        color_continuous_scale="Thermal"
        ).update_traces(hovertemplate='<b>%{location}</b><br>Growth: %{z:.2f}%<extra></extra>',
                       showlegend=False)  # Customize hover template to show only ISO code

    fig.update_geos(
    lakecolor="lightblue",  # Color of lakes
    projection_type="natural earth",
    showlakes=True,  # Ensure that lakes are shown and colored
    bgcolor=background_color
    )
    
    # Increase plot size and remove padding
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Growth<br>Propensity", # Remove the title from the color bar
            titleside="top",
            tickvals=[],            # Remove tick values (i.e., labels)
            ticks='',               # Disable tick marks
            showticklabels=False    # Do not show tick labels
        ),
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    return fig


def plot_usa_states(background_color = "white"):

    # Create a DataFrame for the map
    df = pd.DataFrame({
    'state':  [state.abbr for state in us.states.STATES] + ["DC"],
    'state_name':  [state.name for state in us.states.STATES] + ["District of Columbia"],  # Full state names
    })

    # Assign numerical values to each state (e.g., 0, 1, 2, ...)
    df['value'] = range(len(df))
    
    # Create a custom color scale that maps the numerical values to colors
    colors = custom_color_scale[:len(df)]  # Assuming you have a custom_color_scale
    colorscale = [[i / (len(df) - 1), color] for i, color in enumerate(colors)]
    
    fig = go.Figure(data=go.Choropleth(
        locations = df['state'],  # Spatial coordinates
        locationmode = 'USA-states',  # Set of locations match entries in `locations`
        z = df["value"],  # The numerical data to map to the colorscale
        colorscale = colorscale,  # Custom color scale should be continuous
        colorbar_title = "",  # Title for the color bar
        showscale=False,  # Optionally hide the color bar if not needed
        # hovertemplate='%{location}<extra></extra>'
        hovertext=df['state_name'],  # Show full state name in hover
        hovertemplate='%{hovertext}<extra></extra>',  # Use hovertext (full state name) in hover
    ))
    
    fig.add_scattergeo(
        locations=df['state'],
        locationmode="USA-states",
        text=df['state'],
        mode='text',
        hovertext=df['state_name'],
        hoverinfo='text',
        textfont=dict(
        size=14,  # Increase font size
        color="black",  # Set font color
        family="Arial",  # Font family (optional)
            )
        )
    
    fig.update_layout(
        title_text = '',
        geo_scope='usa', # limite map scope to USA
    )
    
    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=10,  # Set the font size here
            color="Black"
        ),
        geo = dict(showlakes=False)
    )

    # Increase plot size and remove padding
    fig.update_layout(
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    fig.update_geos(
        bgcolor=background_color
    )

    return fig

def plot_usa_states_hotzones(df, background_color = "white"):    
        
    fig = go.Figure(data=go.Choropleth(
        locations = df['state'],  # Spatial coordinates
        locationmode = 'USA-states',  # Set of locations match entries in `locations`
        z = df["Growth"]*100,  # The numerical data to map to the colorscale
        colorscale = "Thermal", 
        colorbar=dict(
            title="Growth<br>Propensity",  # Title for the color bar
            ticks='',  # Disable tick marks
            showticklabels=False  # Hide tick labels
        ),
        # hovertemplate='%{location}<extra></extra>'
        hovertext=df['state_name'],  # Show full state name in hover
        hovertemplate='<b>%{location}</b><br>Growth: %{z:.2f}%<extra></extra>',  # Use hovertext (full state name) in hover
    ))
    
    fig.add_scattergeo(
        locations=df['state'],
        locationmode="USA-states",
        text=df['state'],
        mode='text',
        # hovertext=df['state_name'],
        hoverinfo='skip',
        textfont=dict(
        size=14,  # Increase font size
        # color="white",  # Set font color
        family="Arial",  # Font family (optional)
            )
        )
    
    fig.update_layout(
        title_text = '',
        geo_scope='usa', # limite map scope to USA
    )
    
    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=10,  # Set the font size here
            color="Black"
        ),
        geo = dict(showlakes=False)
    )

    # Increase plot size and remove padding
    fig.update_layout(
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    fig.update_geos(
        bgcolor=background_color
    )

    return fig

## US Counties map
def plot_usa_subnational(state, background_color = "white"):

    # Convert state code to fips code
    fips = fips_codes_state_code[state]

    # Specific state geo data
    counties = us_counties[fips]

    # FIPS to county names
    county_map = {i["properties"]["STATE"] + i["properties"]["COUNTY"]: i["properties"]["NAME"] for i in counties["features"]}

    # Convert to df
    df = pd.DataFrame(county_map.items(), columns=["fips","County"])

    # Assign a unique color to each county
    df['color'] = [custom_color_scale[i % len(custom_color_scale)] for i in range(len(df))]

    # Plot the choropleth map using custom colors and display county name in hover
    fig = px.choropleth(df, 
                        geojson=counties, 
                        locations='fips', 
                        color='color',
                        hover_name='County',  # Display county name in hover
                        color_discrete_sequence=custom_color_scale,
                        scope='usa'
                        ).update_traces(hovertemplate='%{hovertext}<extra></extra>',
                                        showlegend=False)

    if state == "AK":
        fig.update_geos(
            visible=False,  # Hide default geography
            # fitbounds="locations",  # Fit the map bounds to the selected locations
            center={"lat": 62, "lon": -160.4937},  # Centering Alaska (approximate coordinates)
            projection_scale=3.5,  # Adjust this scale for the zoom effect
            showcountries=False,  # Hide country borders
            showcoastlines=False,  # Hide coastlines
            showland=False,  # Hide land coloring (for better focus on counties)
            bgcolor=background_color
    )
    else: # Adjust the layout to focus on the target state
        fig.update_geos(
            visible=False,  # Hide default geography
            fitbounds="locations",  # Fit the map bounds to the selected locations
            showcountries=False,  # Hide country borders
            showcoastlines=False,  # Hide coastlines
            showland=False,  # Hide land coloring (for better focus on counties)
            bgcolor=background_color
        )

    # Increase plot size and remove padding
    fig.update_layout(
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    return fig


def plot_usa_subnational_hotzones(df, state, background_color = "white"):

    # Convert state code to fips code
    fips = fips_codes_state_code[state]

    # Specific state geo data
    counties = us_counties[fips]

    df["Growth"] = df["Growth"]*100

    # Plot the choropleth map using custom colors and display county name in hover
    fig = px.choropleth(df, 
                        geojson=counties, 
                        locations='fips', 
                        color='Growth',
                        hover_name='County',  # Display county name in hover
                        color_continuous_scale="Thermal",
                        scope='usa'
                        ).update_traces(hovertemplate='<b>%{hovertext}</b><br>Growth: %{z:.2f}%<extra></extra>',
                                        showlegend=False)

    if state == "AK":
        fig.update_geos(
            visible=False,  # Hide default geography
            # fitbounds="locations",  # Fit the map bounds to the selected locations
            center={"lat": 62, "lon": -160.4937},  # Centering Alaska (approximate coordinates)
            projection_scale=3.5,  # Adjust this scale for the zoom effect
            showcountries=False,  # Hide country borders
            showcoastlines=False,  # Hide coastlines
            showland=False,  # Hide land coloring (for better focus on counties)
            bgcolor=background_color
    )
    else: # Adjust the layout to focus on the target state
        fig.update_geos(
            visible=False,  # Hide default geography
            fitbounds="locations",  # Fit the map bounds to the selected locations
            showcountries=False,  # Hide country borders
            showcoastlines=False,  # Hide coastlines
            showland=False,  # Hide land coloring (for better focus on counties)
            bgcolor=background_color
        )

    # Increase plot size and remove padding
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Growth<br>Propensity", # Remove the title from the color bar
            titleside="top",
            tickvals=[],            # Remove tick values (i.e., labels)
            ticks='',               # Disable tick marks
            showticklabels=False    # Do not show tick labels
        ),
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=background_color,  # Background color of the plotting area
        paper_bgcolor=background_color,  # Background color of the entire figure
    )

    return fig