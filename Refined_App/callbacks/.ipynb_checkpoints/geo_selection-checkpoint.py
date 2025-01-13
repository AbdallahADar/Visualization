import dash
from dash import html, Input, Output, State
from utils.ids import GEO_FIGURE_IDS, STATE_DATA_ID, SECTOR_NDY_FIGURE_IDS
from utils.constants import APP_BACKGROUND_COLOR, NUTS_COUNTRIES
from utils.styles import TREE_FIGURE
from plots.geo_plot import geo_plot
from plots.tree_plot import tree_plot
from data.StateManager import StateManager
import plotly.graph_objects as go

def register_callbacks(app):
    """
    Register callbacks related to the dashboard page.
    """
    @app.callback(
        [
            Output(GEO_FIGURE_IDS["overall-container"], "style", allow_duplicate=True),
            Output(GEO_FIGURE_IDS["geo-figure"], "figure", allow_duplicate=True),
            Output(GEO_FIGURE_IDS["growth-container"], "style", allow_duplicate=True),
            Output(GEO_FIGURE_IDS["geo-figure-risk"], "figure", allow_duplicate=True),
            Output(GEO_FIGURE_IDS["risk-container"], "style", allow_duplicate=True),
            Output(SECTOR_NDY_FIGURE_IDS["overall-container"], "style", allow_duplicate=True),
            Output(SECTOR_NDY_FIGURE_IDS["tree-figure"], "figure", allow_duplicate=True),            
            Output(STATE_DATA_ID, 'data', allow_duplicate=True)
        ],
        [
            Input(GEO_FIGURE_IDS["geo-figure"], 'clickData'), # If the plot has been clicked
            Input(GEO_FIGURE_IDS["geo-figure-risk"], 'clickData'), # If the plot has been clicked
            State(STATE_DATA_ID, 'data')
        ],
        prevent_initial_call = True
    )
    def update(clicked, clicked_risk, state):

        SM = StateManager.from_dict(state)

        # Will only be triggered if the map is clicked
        if clicked or clicked_risk:

            ## We have different outcomes based on different steps and selections

            if SM.step == "nuts3":
                SM.nuts3 = clicked["points"][0]["location"]
                SM.step = "tree"
                SM.tree_fig = tree_plot(SM.nuts3, "nuts", False, APP_BACKGROUND_COLOR)

            elif SM.step == "nuts2":
                SM.nuts2 = clicked["points"][0]["location"]
                SM.step = "nuts3"

            elif SM.step == "nuts1":
                SM.nuts1 = clicked["points"][0]["location"]
                SM.step = "nuts2"

            elif SM.step == "us_county":
                SM.us_county = clicked["points"][0]["location"]
                SM.step = "tree"
                SM.tree_fig = tree_plot(SM.us_county, "us_counties", False, APP_BACKGROUND_COLOR)

            elif SM.step == "us_state":
                SM.us_state = clicked["points"][0]["location"]
                SM.step = "us_county"
            
            # At country stage
            elif SM.step == "countries":
                
                # Empty the risk plot once country is selected
                SM.geo_fig_risk = {}
                
                # Save country
                SM.country = clicked["points"][0]["location"] if clicked else clicked_risk["points"][0]["location"]
                
                if SM.country == "USA": # Move to states
                    SM.step = "us_state"
                    
                elif SM.country in NUTS_COUNTRIES:
                    SM.step = "nuts1"

                else:
                    SM.step = "tree"
                    SM.tree_fig = tree_plot(SM.country, "countries", False, APP_BACKGROUND_COLOR)

            
            ## Update geo figure
            SM.geo_fig = geo_plot(SM.map_sector, SM, APP_BACKGROUND_COLOR)
            

            print(SM.country, SM.us_state, SM.us_county, SM.nuts1, SM.nuts2, SM.nuts3)
            
            return [dash.no_update if SM.step != "tree" else {'display':'none'}, 
                    SM.geo_fig,
                    {'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'} if SM.step == "us_state" or SM.step == "nuts1" else dash.no_update,
                    SM.geo_fig_risk,
                    {'display':'none'},
                    TREE_FIGURE if SM.step == "tree" else dash.no_update, 
                    SM.tree_fig,
                    SM.to_dict()]

        return []