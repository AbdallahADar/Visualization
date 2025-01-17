import pandas as pd
import numpy as np
import plotly.express as px
from utils.constants import METADATA_COLUMNS, HEATMAP_GEO

def COUNTRY_CHOROPLETH(file_name, bg_color = "white"):

    GROWTH_RATE_COLUMN = METADATA_COLUMNS["GROWTH_RATE_COLUMN"]
    COUNTRY_COLUMN = METADATA_COLUMNS["COUNTRY_COLUMN"]

    ## Read in data
    df = pd.read_csv(file_name)

    ## Change growh rate columns into percentages
    df[GROWTH_RATE_COLUMN] = df[GROWTH_RATE_COLUMN] * 100

    ## Create figure
    fig = px.choropleth(
        df,
        locations = COUNTRY_COLUMN,
        color = GROWTH_RATE_COLUMN,
        hover_name = COUNTRY_COLUMN,
        projection = "natural earth",
        title = "",
        color_continuous_scale = HEATMAP_GEO["hot-zones"]
    )

    ## Custom Hover Format
    fig.update_traces(hovertemplate = '<b>%{location}</b><br>Growth: %{z:.2f}%<extra></extra>',
                       showlegend = False)  # Customize hover template to show only ISO code

    ## Update geo layout
    fig.update_geos(
        lakecolor = "lightblue",  # Color of lakes
        projection_type = "natural earth",
        showlakes = False,  # Ensure that lakes are shown and colored
        bgcolor = bg_color
        )
        
    # Update layout
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Median<br>Growth Rate", # Remove the title from the color bar
            titleside="top",
            tickvals=[],            # Remove tick values (i.e., labels)
            ticks='',               # Disable tick marks
            showticklabels=False    # Do not show tick labels
        ),
        autosize = False,  # Disable automatic sizing
        width = 850,      # Set the width of the figure
        height = 600,      # Set the height of the figure
        margin = dict(l=5, r=5, t=50, b=5),  # Remove padding (left, right, top, bottom)
        plot_bgcolor = bg_color,  # Background color of the plotting area
        paper_bgcolor = bg_color,  # Background color of the entire figure
        clickmode='event+select',
        coloraxis=dict(colorbar=dict(orientation='h', y=-0.2))
        )

    return fig