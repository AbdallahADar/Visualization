import numpy as np
import pandas as pd
from utils.file_names import FILE_NAMES
from plots.geo_plot_sub import COUNTRY_CHOROPLETH, US_STATE_CHOROPLETH, US_COUNTY_CHOROPLETH, NUTS_CHOROPLETH

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