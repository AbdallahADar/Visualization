import dash
from dash import html, Input, Output, State
from utils.ids import STATE_DATA_ID, SECTOR_NDY_FIGURE_IDS, TABLE_COLUMNS, TABLE_IDS
from utils.constants import APP_BACKGROUND_COLOR, NUTS_COUNTRIES, PATH
from utils.styles import TREE_FIGURE, TABLES_CONTAINER
from plots.geo_plot import geo_plot
from plots.tree_plot import tree_plot
from data.StateManager import StateManager
import pandas as pd

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(SECTOR_NDY_FIGURE_IDS["overall-container"], "style", allow_duplicate=True),
            Output(SECTOR_NDY_FIGURE_IDS["tree-figure"], "figure", allow_duplicate=True),
            Output(TABLE_IDS["overall-container"], "style", allow_duplicate=True),
            Output(TABLE_IDS["full-table"], "rowData", allow_duplicate=True),
            Output(STATE_DATA_ID, 'data', allow_duplicate=True)
        ],
        [
            Input(SECTOR_NDY_FIGURE_IDS["tree-figure"], 'clickData'), # If the plot has been clicked
            State(STATE_DATA_ID, 'data')
        ],
        prevent_initial_call = True
    )
    def update(clicked, state):

        SM = StateManager.from_dict(state)

        # Will only be triggered if the tree is clicked
        if clicked:

            if SM.us_county != "":
                data_path = f"{PATH}data/sample_data/Country={'USA'}/State={SM.us_state}/COUNTY_ID={float(SM.us_county)}/data.csv"
            elif SM.nuts3 != "":
                data_path = f"{PATH}data/sample_data/Country={SM.country}/NUTS3_ID={SM.nuts3}/data.csv"
            else:
                data_path = f"{PATH}data/sample_data/Country={SM.country}/data.csv"

            df = pd.read_csv(data_path)
            
            df['Growth'] = df['Growth'].astype(str)
            df['Borrow'] = df['Borrow'].astype(str)
            df['Shrink'] = df['Shrink'].astype(str)

            # Update step
            SM.step = "table"
            
            print(clicked["points"][0])

            ## Get full path of selection
            path = clicked["points"][0]["currentPath"] + clicked["points"][0]["label"]
            path = [i for i in (path).split("/")  if len(i)>0]

            ## Check what filter to apply
            if len(path) == 3:
                SM.sector = path[-2]
                SM.ndy = path[-1]
                df = df[df[TABLE_COLUMNS["ndy"]] == SM.ndy].copy()
                print(SM.sector, SM.ndy)

            elif len(path) == 2:
                SM.sector = path[-1]
                df = df[df[TABLE_COLUMNS["sector"]] == SM.sector].copy()
                print(SM.sector)
            
            return [
                {'display':'none'}, {},
                TABLES_CONTAINER,
                df[list(TABLE_COLUMNS.values())[:-3]].to_dict("records"),
                SM.to_dict()
            ]

        return []
