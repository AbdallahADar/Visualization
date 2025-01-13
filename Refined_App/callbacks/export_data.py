import pandas as pd
import numpy as np
import dash
from dash import html, Input, Output, State, ctx
from utils.ids import TABLE_IDS, DATA_EXPORT_ID

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(TABLE_IDS["selected-table"], 'exportDataAsCsv', allow_duplicate=True),
        ],
        [
            Input(DATA_EXPORT_ID["portfolio-button"], "n_clicks"),
        ],
        prevent_initial_call = True
    )
    def update(n_clicks):
        
        print("export-data")
        
        if n_clicks:
            print("Download")
            return [True]
        
        return [False]