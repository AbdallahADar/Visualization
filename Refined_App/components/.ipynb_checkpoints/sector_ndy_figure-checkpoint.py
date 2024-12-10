import dash
from dash import html, dcc
from utils.ids import SECTOR_NDY_FIGURE_IDS
from plots.placeholder import PLACEHOLDER
import numpy as np
import pandas as pd

## Define container
# Container is filled with placeholder plot

sector_ndy_figure = html.Div(
    id = SECTOR_NDY_FIGURE_IDS["overall-container"],
    style = {'display':'none'},
    children = [
        html.Div(
            dcc.Graph(
                id = SECTOR_NDY_FIGURE_IDS["tree-figure"],
                figure = PLACEHOLDER
            )
        )
    ]
)