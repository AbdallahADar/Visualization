import pandas as pd
import numpy as np
import pycountry
import plotly.express as px
import json
from utils.constants import METADATA_COLUMNS, HEATMAP_GEO
import plotly.graph_objects as go

def NUTS_CHOROPLETH(sector, state, nuts = 1, bg_color = "white"):

    ## Get map sector from state class
    country = state.country
    nuts1 = state.nuts1
    nuts2 = state.nuts2
    country2 = pycountry.countries.get(alpha_3 = country).alpha_2

    print(country, sector, nuts1, nuts2, country2)
    print(f"data/geodata/nuts{nuts}/{country2}.json")

    GROWTH_RATE_COLUMN = METADATA_COLUMNS["GROWTH_RATE_COLUMN"]
    FILTER_COLUMN = METADATA_COLUMNS[f"NUTS{nuts}_FILTER"]
    ID_COLUMN = METADATA_COLUMNS[f"NUTS{nuts}_LOCATION"]
    NUTS_NAME = METADATA_COLUMNS["NUTS_NAME_COLUMN"]

    ## Read in Growth Data
    df = pd.read_csv(f"data/geo_rates/{sector}/nuts{nuts}.csv")

    if nuts == 1:
        geodata = json.load(open(f"data/geodata/nuts{nuts}/{country2}.json"))
        df = df[df[FILTER_COLUMN] == country]

    elif nuts == 2:
        geodata = json.load(open(f"data/geodata/nuts{nuts}/{country2}/{nuts1}.json"))
        geodata = [i for _,i in geodata.items()]
        df = df[df[FILTER_COLUMN] == nuts1]
    
    else:
        geodata = json.load(open(f"data/geodata/nuts{nuts}/{country2}/{nuts1}/{nuts2}.json"))
        geodata = [i for _,i in geodata.items()]
        df = df[df[FILTER_COLUMN] == nuts2]

    fig = px.choropleth(
        df,
        geojson={'type':'FeatureCollection', 'features' : geodata},
        locations = ID_COLUMN,
        color = GROWTH_RATE_COLUMN,  # Color by NUTS region IDs
        featureidkey = "properties.NUTS_ID",
        projection = "mercator",
        title = "",
        color_continuous_scale = HEATMAP_GEO["hot-zones"],
        custom_data = [NUTS_NAME]
        )
    
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Growth: %{z:.2f}%<extra></extra>",
        showlegend=False
        )
    
    # Update the layout to focus on the country and increase the plot size
    fig.update_geos(
        visible=False,
        fitbounds="geojson",
        bgcolor=bg_color
    )
    
    # Increase plot size and remove padding
    fig.update_layout(
        coloraxis=dict(
            colorbar=dict(
            title=dict(
                text="Median<br>Growth Rate",
                side="top"  # This is the correct way to set the title side in recent versions
            ),
            orientation="h",
            y=1.05,
            tickvals=[],            # Remove tick values (i.e., labels)
            ticks='',               # Disable tick marks
            showticklabels=False    # Do not show tick labels
        )),
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=10, r=10, t=10, b=10),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=bg_color,  # Background color of the plotting area
        paper_bgcolor=bg_color,  # Background color of the entire figure
        clickmode='event+select',
    )
        
    return fig