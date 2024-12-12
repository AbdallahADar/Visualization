import numpy as np
import pandas as pd
from utils.file_names import FILE_NAMES
from plots.geo_plot_sub import COUNTRY_CHOROPLETH, COUNTRY_CHOROPLETH_RISK, US_STATE_CHOROPLETH, US_COUNTY_CHOROPLETH, NUTS_CHOROPLETH

## Consolidated function for plots


def geo_plot(sector, state, bg_color):

    # Convert step to file name
    file_name = FILE_NAMES.get(state.step, "")

    ## If Else statements for the different steps

    # Country maps
    if state.step == "countries":
        fig = COUNTRY_CHOROPLETH(f"data/geo_rates/{sector}/{file_name}", bg_color)
    
    elif state.step == "us_state":
        fig = US_STATE_CHOROPLETH(f"data/geo_rates/{sector}/{file_name}", bg_color)

    elif state.step == "us_county":
        fig = US_COUNTY_CHOROPLETH(f"data/geo_rates/{sector}/{file_name}", state.us_state, bg_color)

    elif state.step in ("nuts1", "nuts2", "nuts3"):
        fig = NUTS_CHOROPLETH(sector, state, int(state.step[-1]), bg_color)

    else:
        fig = {}

    return fig

def geo_plot_risk(risk_type, bg_color):

    # Convert step to file name
    file_name = FILE_NAMES.get("countries", "")

    fig = COUNTRY_CHOROPLETH_RISK(f"data/risk_scores/{risk_type}/{file_name}", risk_type, bg_color)

    return fig