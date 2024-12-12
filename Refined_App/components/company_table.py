import dash
from dash import html, dcc
from utils.ids import TABLE_IDS, TABLE_COLUMNS
from utils.constants import SELECTED_TABLE_HEADER
from utils.styles import CELL_STYLING_FUNC_PROPENSITY, CELL_STYLING_EWS
import dash_ag_grid as dag
import numpy as np
import pandas as pd

out = [
    {"headerName":"Company Name", "field": TABLE_COLUMNS["name"], 
     "cellStyle": {"textAlign": "center"},
     "filter": True, "floatingFilter": True, "flex": 1},
    {"headerName": "Location", "field":TABLE_COLUMNS["location"],
     "filter": True, "floatingFilter": True, "flex": 1},
    {"headerName": "Sector", "field":TABLE_COLUMNS["sector"],
     "cellStyle": {"textAlign": "center"},
     "filter": True, "floatingFilter": True, "width": 120, "flex": 1},
    # {"headerName": "Industry", "field":TABLE_COLUMNS["ndy"],
    #  "filter": True, "floatingFilter": True, "flex": 1},
    {"headerName": "Size", "field":TABLE_COLUMNS["size"],
     "cellStyle": {"textAlign": "center"},
     "filter": True, "floatingFilter": True, "width": 120, "flex": 1},
    {"headerName": "EDF-Implied Rating", "field":TABLE_COLUMNS["ir"],
     "cellStyle": {"textAlign": "center"},
     "filter": True, "floatingFilter": True, "flex": 1},
    {"headerName":"Top-Growth Propensity", "field": TABLE_COLUMNS["growth-propensity"],
     "filter": True, "floatingFilter": True,
     # "filterParams":{"values":["True","False"], "caseSensitive": False},
     "cellStyle": {"styleConditions" : CELL_STYLING_FUNC_PROPENSITY, "textAlign": "center"}, "flex": 1},
    # {"headerName":"Borrowing Propensity", "field": TABLE_COLUMNS["borrowing-propensity"],
    #  "filter": True, "floatingFilter": True,
    #  # "filterParams":{"values":["True","False"], "caseSensitive": False},
    #  "cellStyle": {"styleConditions" : CELL_STYLING_FUNC_PROPENSITY, "textAlign": "center"}, "flex": 1},
    # {"headerName":"Shrinkage Propensity", "field": TABLE_COLUMNS["shrinkage-propensity"],
    #  "filter": True, "floatingFilter": True,
    #  # "filterParams":{"values":["True","False"], "caseSensitive": False},
    #  "cellStyle": {"styleConditions" : CELL_STYLING_FUNC_PROPENSITY, "textAlign": "center"}, "flex": 1},
    {"headerName":"Early Warning Signal", "field": TABLE_COLUMNS["ews"],
     "filter": True, "floatingFilter": True,
     # "filterParams":{"values":["Low","Medium","High","Severe"], "caseSensitive": False},
     "cellStyle": {"styleConditions" : CELL_STYLING_EWS, "textAlign": "center"}, "flex": 1}
    ]

defaultColDef = {
    "initialWidth": 200,
    "wrapHeaderText": True,
    "autoHeaderHeight": True,
}

company_table = html.Div(
    id = TABLE_IDS["overall-container"],
    style = {"display":"none"},
    children = [
        html.H1("", style = {"text-align":"center"}),
        dag.AgGrid(
            id = TABLE_IDS["full-table"],
            columnDefs = out,
            rowData = [],
            defaultColDef=defaultColDef,
            dashGridOptions = {
                "pagination": True,
                "paginationPageSize": 20,
                "rowSelection": "single"  # Single selection to add row by row
                }
            ),
        html.Div([
            html.H2(SELECTED_TABLE_HEADER, style = {'text-align': 'center', 'display': 'inline-block'}),
            html.Button("Export as csv", id = "portfolio-selection-button", 
                        n_clicks = 0,
                        style = {
                               "margin-left": "20px",
                                "padding": "8px 16px",
                                "font-size": "1em",
                                "color": "white",
                                "background-color": "#3399ff",
                                "border": "none",
                                "border-radius": "5px",
                                "cursor": "pointer",
                                "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",
                                "display": "inline-block",
                                "vertical-align": "middle"
                               })
            ], 
                 style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                 ),
            dag.AgGrid(
                id = TABLE_IDS["selected-table"],
                columnDefs = out,
                rowData = [],
                defaultColDef=defaultColDef,
                csvExportParams = {"fileName" : "screened_names.csv"},
                dashGridOptions={
                    "pagination": True,
                    "paginationPageSize": 20,
                    "rowSelection": "single"  # Single selection to add row by row
                    }
                ),
        ]
)