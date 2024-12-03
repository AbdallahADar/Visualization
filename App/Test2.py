import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import dash_daq as daq
import pandas as pd
import json
import numpy as np
import itertools
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend

import Network_Plots as NPlots
import Driver_Plots as DPlots
import DistMatrix_Plots as DMPlots
import Silhouette_Plots as SPlots
import RadarMeter_Plots as RPlots
import Geographical_Plots as GPlots
import AppSetup_Optimized as AppSetup
import Setup
from Setup import OKAY_BUTTON_STYLE, SECTOR_CONTAINER_STYLE, COLOR_BUTTON_STYLE, BOX_STYLE_FULL, HOVER_STYLE, PRINT_STYLE, APP_BACKGROUND_COLOR, NEXT_BUTTON_STYLE, model_type_list, category_colors, sectors_ndy


app = dash.Dash(__name__)

app.index_string = Setup.index_string

# Layout of the app
app.layout = html.Div(
    
    id = "app-container",
    
    children = [
    dcc.Store(id = "state-manager"), # Stored data full

    html.Div(
        id = "start-page",
        children = [
            # Left half for exploratory search
            html.Div(
                id = "exploratory-half",
                children = html.H2("Exploratory Search",
                                  style = {'color': 'white', 'font-size': '2.5em'}),
                style = Setup.exploratory_half,
            ),
            # Right half for targeted search
            html.Div(
                id = "targeted-half",
                children = html.H2("Targeted Search",
                                  style = {'color': 'white', 'font-size': '2.5em'}),
                style = Setup.targeted_half,
            ),
        ],
        style = {'display': 'flex', 'height': '100vh', 'overflow': 'hidden'}
    ),

    html.Div([],style = {'marginTop': '10px'},    # Add distance from the top of the page
    ),

    # Geographical plots container
        html.Div([
    dcc.Graph(id = 'map', 
                  # figure = GPlots.plot_global_country(background_color = APP_BACKGROUND_COLOR).update_layout(clickmode='event+select'),
                  figure = AppSetup.placeholder(),
                  style =  {"display":"none"}
                 ),
        ],style = {'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center'
                  }
                )
    ]
    )

@app.callback(
    [Output("start-page", "style"),
     # Output("exploratory-half", "style"),
     # Output("targeted-half", "style")
     Output("map", "figure"),
     Output("map", "style"),
    ],
    [Input("exploratory-half", "n_clicks"),
     Input("targeted-half", "n_clicks")]
)
def navigate_pages(exploratory_clicks, targeted_clicks):
    # Define base styles for both sides
    # Check which side was clicked
    if exploratory_clicks:
        # Expand the left side to cover the screen
        return ({"display":"none"},GPlots.plot_global_country(background_color = APP_BACKGROUND_COLOR).update_layout(clickmode='event+select'),
                {**Setup.geofig_styling, 
                          "background-color":APP_BACKGROUND_COLOR}
        )
    elif targeted_clicks:
        pass

    # Default split view for the start page
    return (dash.no_update,dash.no_update, dash.no_update
    )

if __name__ == "__main__":
    app.run_server(debug=True)