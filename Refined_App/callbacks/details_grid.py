import pandas as pd
import numpy as np
import dash
from dash import html, Input, Output, State
from utils.ids import DETAILS_POP_UP_IDS, DETAILS_GRID_IDS
from utils.constants import TOTAL_CELLS, GRID_CONTENT

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(DETAILS_POP_UP_IDS["overall-container"], "is_open", allow_duplicate=True),
            Output(DETAILS_POP_UP_IDS["body"], "children", allow_duplicate=True),
        ],
        [
            Input(DETAILS_GRID_IDS[f"G{i}"], "n_clicks") for i in range(1, TOTAL_CELLS+1)
        ] + [Input(DETAILS_POP_UP_IDS["button"], "n_clicks")],
        [
            State(DETAILS_POP_UP_IDS["overall-container"], 'is_open')
        ],
        prevent_initial_call = True
    )
    def update(*args):

        print("details-grid")

        ctx = dash.callback_context
        # Identify which component triggered the callback
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        print(triggered_id)

        grid_clicks = args[:-TOTAL_CELLS]
        close_click = args[-2]
        is_open = args[-1]

        # Close button is clicked, close the pop-up
        if triggered_id == DETAILS_POP_UP_IDS["button"]:
            print(close_click)
            return False, []
            
        # Check which grid cell was clicked
        for i, click in enumerate(grid_clicks):
            if triggered_id == DETAILS_GRID_IDS[f"G{i+1}"]:
                return True, GRID_CONTENT[f"G{i+1}"]

        return is_open, dash.no_update