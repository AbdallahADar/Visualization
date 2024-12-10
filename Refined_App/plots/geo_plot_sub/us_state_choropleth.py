import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.constants import METADATA_COLUMNS

def US_STATE_CHOROPLETH(file_name, bg_color = "white"):

    GROWTH_RATE_COLUMN = METADATA_COLUMNS["GROWTH_RATE_COLUMN"]
    STATE_COLUMN = METADATA_COLUMNS["STATE_COLUMN"]
    STATE_NAME = METADATA_COLUMNS["STATE_NAME_COLUMN"]

    ## Read in data
    df = pd.read_csv(file_name)

    ## Change growh rate columns into percentages
    df[GROWTH_RATE_COLUMN] = df[GROWTH_RATE_COLUMN] * 100

    ## Create figure
    fig = go.Figure(
        data = go.Choropleth(
            locations = df[STATE_COLUMN],  # Spatial coordinates
            locationmode = 'USA-states',  # Set of locations match entries in `locations`
            z = df[GROWTH_RATE_COLUMN],  # The numerical data to map to the colorscale
            colorscale = "Thermal", 
            colorbar=dict(
                title="Median<br>Growth Rate",  # Title for the color bar
                ticks='',  # Disable tick marks
                showticklabels=False  # Hide tick labels
            ),
            hovertext=df[STATE_NAME],  # Show full state name in hover
            hovertemplate='<b>%{location}</b><br>Growth: %{z:.2f}%<extra></extra>',  # Use hovertext (full state name) in hover
    ))

    ## Add Names of the States
    fig.add_scattergeo(
        locations = df[STATE_COLUMN],
        locationmode="USA-states",
        text = df[STATE_COLUMN],
        mode='text',
        hoverinfo='skip',
        textfont=dict(
            size=14,  # Increase font size
            family="Arial",  # Font family (optional)
            )
    )
        

    ## Update layout
    fig.update_layout(
        title_text = '',
        geo_scope='usa', # limite map scope to USA
        font=dict(
            family="Courier New, monospace",
            size=10,  # Set the font size here
            color="Black"
        ),
        geo = dict(showlakes=False),
        autosize=False,  # Disable automatic sizing
        width=1000,      # Set the width of the figure
        height=600,      # Set the height of the figure
        margin=dict(l=5, r=5, t=5, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor=bg_color,  # Background color of the plotting area
        paper_bgcolor=bg_color,  # Background color of the entire figure
        clickmode='event+select'
    )

    ## Update geo layout
    fig.update_geos(
        bgcolor=bg_color
    )

    return fig