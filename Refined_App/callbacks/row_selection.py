import pandas as pd
import numpy as np
import dash
from dash import html, Input, Output, State, ctx
from utils.ids import STATE_DATA_ID, TABLE_COLUMNS, TABLE_IDS
from data.StateManager import StateManager

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(TABLE_IDS["selected-table"], 'rowData', allow_duplicate=True),
            Output(STATE_DATA_ID, 'data', allow_duplicate=True)
        ],
        [
            Input(TABLE_IDS["full-table"], "selectedRows"),
            State(STATE_DATA_ID, 'data')
        ],
        prevent_initial_call = True
    )
    def update(selection, state):
        
        print("row-selection")
        
        if selection:
            
            SM = StateManager.from_dict(state)
     
            if selection[0] not in SM.selected_rows:
                SM.selected_rows.append(selection[0])
                
            return SM.selected_rows, SM.to_dict()
        
        return dash.no_update, dash.no_update