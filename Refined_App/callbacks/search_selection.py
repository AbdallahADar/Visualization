import dash
from dash import html, Input, Output, State
from utils.ids import SEARCH_SELECTION_IDS, GEO_FIGURE_IDS, STATE_DATA_ID
from utils.constants import APP_BACKGROUND_COLOR
from utils.styles import GEO_FIGURE
from plots.geo_plot import geo_plot
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
            return [{'display':'none'}, [], 
                    GEO_FIGURE, SM.geo_fig,
                    SM.to_dict()]
        elif target:
            return [dash.no_update, [html.H1("Target")], 
                    dash.no_update, SM.geo_fig,
                    SM.to_dict()]

        return []