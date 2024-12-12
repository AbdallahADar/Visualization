import pandas as pd
import numpy as np
import dash
from dash import html, Input, Output, State
from utils.ids import SEARCH_SELECTION_IDS, GEO_FIGURE_IDS, STATE_DATA_ID, TABLE_COLUMNS, TABLE_IDS
from utils.constants import APP_BACKGROUND_COLOR
from utils.styles import GEO_FIGURE, TABLES_CONTAINER
from plots.geo_plot import geo_plot, geo_plot_risk
from data.StateManager import StateManager

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(SEARCH_SELECTION_IDS["overall-container"], "style"),
            Output(SEARCH_SELECTION_IDS["overall-container"], "children"),
            Output(GEO_FIGURE_IDS["overall-container"], "style", allow_duplicate=True),
            Output(GEO_FIGURE_IDS["geo-figure"], "figure", allow_duplicate=True),
            Output(GEO_FIGURE_IDS["geo-figure-risk"], "figure", allow_duplicate=True),
            Output(TABLE_IDS["overall-container"], "style", allow_duplicate=True),
            Output(TABLE_IDS["full-table"], "rowData", allow_duplicate=True),
            Output(STATE_DATA_ID, 'data', allow_duplicate=True)
        ],
        [
            Input(SEARCH_SELECTION_IDS["exploratory-block"], "n_clicks"),
            Input(SEARCH_SELECTION_IDS["targeted-block"], "n_clicks"),
            State(STATE_DATA_ID, 'data')
        ],
        prevent_initial_call = True
    )
    def update(exploratory, target, state):

        print("search-selection")

        SM = StateManager.from_dict(state) if state else StateManager()

        # Exploratory selected
        if exploratory:
            SM.step = "countries"
            SM.geo_fig = geo_plot("All", SM, APP_BACKGROUND_COLOR)
            SM.geo_fig_risk = geo_plot_risk("Overall Risk", APP_BACKGROUND_COLOR)
            return [{'display':'none'}, [], 
                    GEO_FIGURE, SM.geo_fig,SM.geo_fig_risk,
                    dash.no_update, [],
                    SM.to_dict()]
        elif target:
            
            ## Read in Sample data for now
            data_path1 = f"data/sample_data/Country={'USA'}/State=NJ/COUNTY_ID={float(34023)}/data.csv"
            df1 = pd.read_csv(data_path1)
            data_path2 = f"data/sample_data/Country={'JPN'}/data.csv"
            df2 = pd.read_csv(data_path2)
            data_path3 = f"data/sample_data/Country={'BRA'}/data.csv"
            df3 = pd.read_csv(data_path3)
            
            df = pd.concat([df3, df2, df1])
            df['Growth'] = df['Growth'].astype(str)
            df['Borrow'] = df['Borrow'].astype(str)
            df['Shrink'] = df['Shrink'].astype(str)
            
            return [{'display':'none'}, [],
                    dash.no_update, {},{},
                    TABLES_CONTAINER,
                    df[list(TABLE_COLUMNS.values())[:-3]].to_dict("records"),
                    SM.to_dict()]

        return []