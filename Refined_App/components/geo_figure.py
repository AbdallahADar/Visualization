import dash
from dash import html, dcc
from utils.ids import GEO_FIGURE_IDS
from utils.constants import SECTORS_ALL, RISK_SCORES
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
            id = GEO_FIGURE_IDS["growth-container"],
            style = {'width' : '48%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
            children = [
            html.Div(
                dcc.Graph(
                    id = GEO_FIGURE_IDS["geo-figure"],
                    figure = PLACEHOLDER
                )
            ),
            html.Div(
                dcc.Dropdown(
                    options = SECTORS_ALL,
                    value = "All",
                    clearable = False,
                    id = GEO_FIGURE_IDS["sector-dropdown"],
                    ),
                style = {'width': '25%'}
            )
        ]),
        html.Div(
            id = GEO_FIGURE_IDS["risk-container"],
            style = {'width' : '48%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
            children = [
            html.Div(
                dcc.Graph(
                    id = GEO_FIGURE_IDS["geo-figure-risk"],
                    figure = PLACEHOLDER
                )
            ),
            html.Div(
                dcc.Dropdown(
                    options = RISK_SCORES,
                    value = "Overall Risk",
                    clearable = False,
                    id = GEO_FIGURE_IDS["risk-dropdown"],
                    ),
                style = {'width': '25%'}
            )
        ])
    ]
)