import dash
from dash import callback_context
from dash import dcc, html, Input, Output, State
import dash_ag_grid as dag
import pandas as pd
import random

app = dash.Dash(__name__)

# Cell styling rules for conditional coloring
cell_styling_func = [
    {"condition": "params.value === 'H'", "style": {"backgroundColor": "Green", 'color': 'Green'}},
    {"condition": "params.value === 'MH'", "style": {"backgroundColor": "Yellow", 'color': 'Yellow'}},
    {"condition": "params.value === 'ML'", "style": {"backgroundColor": "Orange", 'color': 'Orange'}},
    {"condition": "params.value === 'L'", "style": {"backgroundColor": "Red", 'color': 'Red'}},
]

# Dummy data (replace with actual data source or backend connection)
data = pd.DataFrame({
    "Name": [f"Name {i}" for i in range(1000000)],
    "Value": range(1000000),
    "Country": [random.choice(["USA", "Canada", "Mexico", "Germany", "France"]) for _ in range(1000000)],
    "Sector": [random.choice(["Tech", "Finance", "Healthcare", "Energy", "Consumer"]) for _ in range(1000000)],
    "Size": [random.choice(["Large", "Medium", "Small"]) for _ in range(1000000)],
    "Sales Propensity": [random.choice(["H", "MH", "ML", "L"]) for _ in range(1000000)],
    "Asset Propensity": [random.choice(["H", "MH", "ML", "L"]) for _ in range(1000000)],
    "Borrow Propensity": [random.choice(["H", "MH", "ML", "L"]) for _ in range(1000000)],
    "Shrink Propensity": [random.choice(["H", "MH", "ML", "L"]) for _ in range(1000000)]
})

# Layout
app.layout = html.Div([

    # Starting page with split screen effect
    html.Div(id="start-page", style={'display': 'flex', 'height': '100vh', 'overflow': 'hidden'}, children=[
        # Left half for Exploratory Search
        html.Div(
            id="exploratory-half",
            children=html.H2("Exploratory Search", style={'color': 'white', 'font-size': '2.5em'}),
            style={
                'flex': '1', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                'background-color': '#007BFF', 'cursor': 'pointer', 'transition': 'flex 0.6s ease',
                'position': 'relative', 'height': '100%'
            },
        ),
        # Right half for Targeted Search
        html.Div(
            id="targeted-half",
            children=html.H2("Targeted Search", style={'color': 'white', 'font-size': '2.5em'}),
            style={
                'flex': '1', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                'background-color': '#28A745', 'cursor': 'pointer', 'transition': 'flex 0.6s ease',
                'position': 'relative', 'height': '100%'
            },
        ),
    ]),

    html.Div(id = "target-search", style = {"display":"none"},
             children = [
    html.H1("Global Portfolio", id="header", style={'text-align': 'center'}),
    
    # Main data table with multi-row selection enabled and filters on each column
    dag.AgGrid(
        id="data-grid",
        columnDefs=[
            {"field": "Name", "filter": True, "floatingFilter": True, "flex": 1},
            {"field": "Value", "filter": True, "floatingFilter": True, "flex": 1},
            {"field": "Country", "filter": True, "floatingFilter": True, "width": 120, "flex": 1},
            {"field": "Sector", "filter": True, "floatingFilter": True, "flex": 1},
            {"field": "Size", "filter": True, "floatingFilter": True, "width": 120, "flex": 1},
            {"field": "Sales Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
            {"field": "Asset Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
            {"field": "Borrow Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
            {"field": "Shrink Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
        ],
        rowData=data.head(100).to_dict("records"),  # Load initial rows
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,
            "rowSelection": "single"  # Single selection to add row by row
        }
    ),
    
    # html.H2("Selected Portfolio", id="selected-header", style={'text-align': 'center'}),
    html.Div([
    html.H2("Selected Portfolio", id="selected-header", style={'text-align': 'center', 'display': 'inline-block'}),
    html.Button("Done", id="done-button", n_clicks=0, style={
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
], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    # Table to display selected rows
    dag.AgGrid(
        id="selected-rows-grid",
        columnDefs=[
            {"field": "Name", "filter": True, "floatingFilter": True, "flex": 1},
            {"field": "Value", "filter": True, "floatingFilter": True, "flex": 1},
            {"field": "Country", "filter": True, "floatingFilter": True, "width": 120, "flex": 1},
            {"field": "Sector", "filter": True, "floatingFilter": True, "flex": 1},
            {"field": "Size", "filter": True, "floatingFilter": True, "width": 120, "flex": 1},
            {"field": "Sales Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
            {"field": "Asset Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
            {"field": "Borrow Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
            {"field": "Shrink Propensity", "filter": True, "floatingFilter": True,"cellStyle": {"styleConditions" : cell_styling_func}, "flex": 1},
        ],
        rowData=[],  # Start empty, will populate with selected rows
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,
            "rowSelection": "single"  # Single selection to add row by row
        }
    ),
             ]),
    
    dcc.Store(id="selected-rows-store", storage_type="memory"),
    html.Button("Done", id="done-button", n_clicks=0, style={"margin": "20px"}),
    html.Div(id="end-message", style={'text-align': 'center', 'display': 'none'})
])

# Callback for loading filtered rows based on input
@app.callback(
    Output("data-grid", "rowData"),
    Input("data-grid", "filterModel"),
    prevent_initial_call=True
)
def filter_rows(filter_model):
    filtered_data = data
    
    # Apply filters from each column if present
    for column, filter_info in (filter_model or {}).items():
        if "filter" in filter_info:
            filter_value = filter_info["filter"]
            # Apply filter to each column as case-insensitive substring search
            filtered_data = filtered_data[filtered_data[column].str.contains(filter_value, case=False, na=False)]
    
    return filtered_data.head(100).to_dict("records")

# Callback to update selected rows grid with stored data
@app.callback(
    Output("selected-rows-grid", "rowData"),
    Input("selected-rows-store", "data"),
    prevent_initial_call=True
)
def display_selected_rows(selected_rows_data):
    return selected_rows_data if selected_rows_data else []


@app.callback(
    Output("selected-rows-store", "data"),
    [Input("data-grid", "selectedRows"), Input("selected-rows-grid", "selectedRows")],
    State("selected-rows-store", "data"),
    prevent_initial_call=True
)
def update_selected_rows(data_grid_selection, selected_rows_grid_selection, stored_rows):
    # Initialize stored_rows if it's None
    if stored_rows is None:
        stored_rows = []

    # Determine which input triggered the callback
    triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]

    print(triggered_id)

    if triggered_id == "data-grid" and data_grid_selection:
        # Add row if selected in main grid and not already in stored_rows
        if data_grid_selection[0] not in stored_rows:
            stored_rows.append(data_grid_selection[0])

    elif triggered_id == "selected-rows-grid" and selected_rows_grid_selection:
        # Remove row if selected in selected-rows-grid and exists in stored_rows
        stored_rows = [row for row in stored_rows if row != selected_rows_grid_selection[0]]

    return stored_rows

# Callback to display "The End" message
@app.callback(
    [Output("header", "style"),
     Output("data-grid", "style"),
     Output("selected-header", "style"),
     Output("selected-rows-grid", "style"),
     Output("done-button", "style"),
     Output("end-message", "style")],
    Input("done-button", "n_clicks")
)
def display_end_message(n_clicks):
    if n_clicks > 0:
        # Hide all other components, show "The End" message
        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "block"}
        )
    else:
        # Show all components, hide "The End" message
        return (
            {"display": "block"},
            {"display": "block"},
            {"display": "block"},
            {"display": "block"},
            {"display": "block"},
            {"display": "none"}
        )

# Callback to handle transitions between pages
@app.callback(
    [Output("start-page", "style"),
     Output("target-search", "style"),
     Output("exploratory-half", "style"),
     Output("targeted-half", "style")],
    [Input("exploratory-half", "n_clicks"),
     Input("targeted-half", "n_clicks")]
)
def navigate_pages(exploratory_clicks, targeted_clicks):
    # Define base styles for both sides
    base_style = {
        'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
        'cursor': 'pointer', 'position': 'relative', 'height': '100%', 'transition': 'flex 10s ease',
    }
    
    # Check which side was clicked
    if exploratory_clicks:
        # Expand the left side to cover the screen
        return (
            {'display': 'none'}, {'display': 'none'},
            {**base_style, 'flex': '3', 'background-color': '#007BFF'}, 
            {**base_style, 'flex': '0'}
        )
    elif targeted_clicks:
        # Expand the right side to cover the screen
        return (
            {'display': 'none'}, {'display': 'flex',"alignItems": "center",
        "justifyContent": "center","flexDirection": "column"},
            {**base_style, 'flex': '0'},
            {**base_style, 'flex': '3', 'background-color': '#28A745'}
        )

    # Default split view for the start page
    return (dash.no_update,dash.no_update,dash.no_update,dash.no_update
    )

if __name__ == "__main__":
    app.run_server(debug=True)