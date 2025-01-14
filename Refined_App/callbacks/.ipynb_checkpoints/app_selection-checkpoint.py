import pandas as pd
import numpy as np
import dash
from dash import html, Input, Output, State
from utils.ids import APP_SELECTION_IDS, SEARCH_SELECTION_IDS, STATE_DATA_ID, DETAILS_GRID_IDS
from utils.constants import APP_BACKGROUND_COLOR
from utils.styles import SELECTION_CONTAINER
from data.StateManager import StateManager

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(APP_SELECTION_IDS["overall-container"], "style", allow_duplicate=True),
            Output(APP_SELECTION_IDS["overall-container"], "children", allow_duplicate=True),
            Output(SEARCH_SELECTION_IDS["overall-container"], "style", allow_duplicate=True),
            Output(DETAILS_GRID_IDS["overall-container"], "style", allow_duplicate=True)
        ],
        [
            Input(APP_SELECTION_IDS["demo-block"], "n_clicks"),
            Input(APP_SELECTION_IDS["details-block"], "n_clicks"),
            State(STATE_DATA_ID, 'data')
        ],
        prevent_initial_call = True
    )
    def update(demo, details, state):

        print("app-mode")

        SM = StateManager.from_dict(state) if state else StateManager()

        # Demo selected
        if demo:
            SM.step = "demo"
            # Hide the app mode selection page and display the search selection page
            return [{'display':'none'}, [], 
                    SELECTION_CONTAINER, {'display':'none'}]
        elif details:
            SM.step = "details"
            return [{'display':'none'}, [],
                    dash.no_update, {'display':'flex'}]

        return []