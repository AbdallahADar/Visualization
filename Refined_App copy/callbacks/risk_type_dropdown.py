import dash
from dash import html, Input, Output, State
from utils.ids import GEO_FIGURE_IDS, STATE_DATA_ID
from utils.constants import APP_BACKGROUND_COLOR
from plots.geo_plot import geo_plot_risk
from data.StateManager import StateManager

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(GEO_FIGURE_IDS["geo-figure-risk"], 'figure', allow_duplicate=True),
            Output(STATE_DATA_ID, 'data', allow_duplicate=True),
        ],
        [
            Input(GEO_FIGURE_IDS["risk-dropdown"], 'value'),
            State(STATE_DATA_ID, 'data')
            ],
        prevent_initial_call = True
    )
    def update(risk_type, state):

        print("risk-type-dropdown")

        SM = StateManager.from_dict(state)
        SM.risk_type = risk_type

        # Update figure based on sector and step
        SM.geo_fig_risk = geo_plot_risk(risk_type, APP_BACKGROUND_COLOR)
    
        return SM.geo_fig_risk, SM.to_dict()