from utils.constants import TOTAL_CELLS

## Save container IDs for usage

APP_SELECTION_IDS = {
    'overall-container' : 'app-selection-page',
    'demo-block' : 'demo-half',
    'details-block' : 'details-half',
}

SEARCH_SELECTION_IDS = {
    'overall-container' : 'seearch-selection-page',
    'exploratory-block' : 'exploratory-half',
    'targeted-block' : 'taregeted-half',
}

GEO_FIGURE_IDS = {
    'overall-container' : 'geo-page',
    'risk-container' : 'risk-container',
    'growth-container' : 'growth-container',
    'geo-figure' : 'geo-plot',
    'sector-dropdown' : 'sector-dropdown',
    'geo-figure-risk' : 'geo-plot-risk',
    'risk-dropdown' : 'risk-dropdown',
}

SECTOR_NDY_FIGURE_IDS = {
    'overall-container' : 'sector-ndy-page',
    'tree-figure' : 'tree-plot',
}

STATE_DATA_ID = 'state-class'

TABLE_IDS = {
    'overall-container' : 'table-page',
    'full-table' : 'full-table',
    'selected-table' : 'screened-table'
}

TABLE_COLUMNS = {
    "name": "Name",
    "location":"Location",
    "sector":"Sector",
    # "ndy":"Industry",
    "size":"Size",
    "growth-propensity":"Growth",
    # "borrowing-propensity":"Borrow",
    # "shrinkage-propensity":"Shrink",
    "ir":"IR",
    "ews":"EWS",
    "nuts":"NUTS3_ID",
    "us_county":"COUNTY_ID",
    "country" : "COUNTRY"
}

DATA_EXPORT_ID = {
    "portfolio-button" : "portfolio-selection-button"
}

DETAILS_GRID_IDS = {f"G{i}":f"grid-{i}" for i in range(1, TOTAL_CELLS+1)}
DETAILS_GRID_IDS["overall-container"] = "details-grid"

DETAILS_POP_UP_IDS = {
    "overall-container":"pop-up-container",
    "body":"pop-up-body",
    "button":"pop-up-close-button",
}