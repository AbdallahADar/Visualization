import dash
from dash import html, dcc
from utils.ids import GEO_FIGURE_IDS
from utils.constants import SECTORS
from plots.placeholder import PLACEHOLDER
import numpy as np
import pandas as pd

## Define container
# Container is filled with placeholder plot

geo_figure = html.Div(
    id = GEO_FIGURE_IDS["overall-container"],
    style = {'display':'none'},
    children = [
        html.Div(
            dcc.Graph(
                id = GEO_FIGURE_IDS["geo-figure"],
                figure = PLACEHOLDER
            )
        ),
        html.Div(
            dcc.Dropdown(
                options = SECTORS,
                value = "All",
                clearable = False,
                id = GEO_FIGURE_IDS["sector-dropdown"],
                ),
            style = {'width': '10%'}
        )
    ]
)