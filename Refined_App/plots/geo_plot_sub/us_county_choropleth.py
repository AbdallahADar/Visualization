import pandas as pd
import numpy as np
import plotly.express as px
from utils.constants import METADATA_COLUMNS, HEATMAP_GEO, PATH
import json

def US_COUNTY_CHOROPLETH(file_name, state, bg_color = "white"):

    GROWTH_RATE_COLUMN = METADATA_COLUMNS["GROWTH_RATE_COLUMN"]
    COUNTY_COLUMN = METADATA_COLUMNS["COUNTY_COLUMN"]
    COUNTY_NAME = METADATA_COLUMNS["COUNTY_NAME_COLUMN"]

    df = pd.read_csv(file_name)

    # Sometimes strings removing leading zeros when read in as numeric
    df[COUNTY_COLUMN] = df[COUNTY_COLUMN].apply(lambda x: "0"+str(x) if len(str(x)) == 4 else x)

    ## Read in geodata
    file = f"{PATH}data/geodata/us_counties/{state}.json"
    counties = json.load(open(file))

    # Plot the choropleth map using custom colors and display county name in hover
    fig = px.choropleth(df, 
                        geojson = {'type':'FeatureCollection', 'features' : counties}, 
                        locations = COUNTY_COLUMN, 
                        color = GROWTH_RATE_COLUMN,
                        hover_name = COUNTY_NAME,  # Display county name in hover
                        color_continuous_scale = HEATMAP_GEO["hot-zones"],
                        scope = 'usa'
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
            bgcolor=bg_color
    )
    else: # Adjust the layout to focus on the target state
        fig.update_geos(
            visible=False,  # Hide default geography
            fitbounds="locations",  # Fit the map bounds to the selected locations
            showcountries=False,  # Hide country borders
            showcoastlines=False,  # Hide coastlines
            showland=False,  # Hide land coloring (for better focus on counties)
            bgcolor=bg_color
        )

    # Increase plot size and remove padding
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Median<br>Growth Rate", # Remove the title from the color bar
            titleside="top",
            tickvals=[],            # Remove tick values (i.e., labels)
            ticks='',               # Disable tick marks
            showticklabels=False    # Do not show tick labels
        ),
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=bg_color,  # Background color of the plotting area
        paper_bgcolor=bg_color,  # Background color of the entire figure
        clickmode='event+select'
    )

    return fig