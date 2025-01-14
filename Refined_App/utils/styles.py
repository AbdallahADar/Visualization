from utils.constants import COLORS, FONTS, FONT_SIZES, PROPENSITY_COLOR, EWS_COLOR 

########### App Index String ###########
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;  /* Ensure the body and html take up full viewport height */
            }
            #app-container {
                height: 100vh;  /* Make the app container take up the full viewport height */
                display: flex;
                flex-direction: column;
            }
        </style>
    </head>
    <body>
        <div id="app-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

########### Search Selection Page ###########

SELECTION_CONTAINER = {
    'display': 'flex', 
    'height' : '100vh',
    'overflow' : 'hidden',
}

DEMO_SELECTION_HALF = {
    'flex': '1', 
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center',
    'background-color': COLORS["demo_block"], 
    'cursor': 'pointer', 
    'transition': 'flex 0.6s ease',
    'position': 'relative', 
    'height': '100%'
}

DEMO_SELECTION_HEADER = {
    'color' : COLORS["demo_text"],
    'font-family' : f"{FONTS['headings']}, {FONTS['headings-fallback']}",
    'font-size' : FONT_SIZES["demo_text"]
}

DETAILS_SELECTION_HALF = {
    'flex': '1', 
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center',
    'background-color': COLORS["details_block"], 
    'cursor': 'pointer', 
    'transition': 'flex 0.6s ease',
    'position': 'relative', 
    'height': '100%'
}

DETAILS_SELECTION_HEADER = {
    'color' : COLORS["details_text"],
    'font-family' : f"{FONTS['headings']}, {FONTS['headings-fallback']}",
    'font-size' : FONT_SIZES["details_text"]
}

########### Search Selection Page ###########

EXPLORATORY_SELECTION_HALF = {
    'flex': '1', 
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center',
    'background-color': COLORS["exploratory_block"], 
    'cursor': 'pointer', 
    'transition': 'flex 0.6s ease',
    'position': 'relative', 
    'height': '100%'
}

EXPLORATORY_SELECTION_HEADER = {
    'color' : COLORS["exploratory_text"],
    'font-family' : f"{FONTS['headings']}, {FONTS['headings-fallback']}",
    'font-size' : FONT_SIZES["exploratory_text"]
}

TARGETED_SELECTION_HALF = {
    'flex': '1', 
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'center',
    'background-color': COLORS["targeted_block"], 
    'cursor': 'pointer', 
    'transition': 'flex 0.6s ease',
    'position': 'relative', 
    'height': '100%'
}

TARGETED_SELECTION_HEADER = {
    'color' : COLORS["targeted_text"],
    'font-family' : f"{FONTS['headings']}, {FONTS['headings-fallback']}",
    'font-size' : FONT_SIZES["targeted_text"]
}

########### Global, Country, Sub-Country, Sector & NDY Graph Pages ###########

GEO_FIGURE = {
    'display': 'flex',
    'justifyContent': 'center',  # Horizontally center the graph
    'alignItems': 'center', # Vertically center the graph
    'margin-bottom':'5px',
    'flex-direction': 'row',
    # 'marginLeft': 'auto', 'marginRight': 'auto'
}

TREE_FIGURE = {
    'display': 'flex',
    'justifyContent': 'center',  # Horizontally center the graph
    'alignItems': 'center', # Vertically center the graph
    'margin-bottom':'5px',
    # 'marginLeft': 'auto', 'marginRight': 'auto'
}

########### Tables Page ###########

CELL_STYLING_FUNC_PROPENSITY = [
    {"condition": "params.value === 'True'", 
     "style": {"backgroundColor": PROPENSITY_COLOR["T"], 'color': PROPENSITY_COLOR["T"]}},
    {"condition": "params.value === 'False'", 
     "style": {"backgroundColor": PROPENSITY_COLOR["F"], 'color': PROPENSITY_COLOR["F"]}},
]


CELL_STYLING_EWS = [
    {"condition": "params.value === 'Low'", 
     "style": {"backgroundColor": EWS_COLOR["L"], 'color': EWS_COLOR["L"]}},
    {"condition": "params.value === 'Medium'", 
     "style": {"backgroundColor": EWS_COLOR["M"], 'color': EWS_COLOR["M"]}},
    {"condition": "params.value === 'High'", 
     "style": {"backgroundColor": EWS_COLOR["H"], 'color': EWS_COLOR["H"]}},
    {"condition": "params.value === 'Severe'", 
     "style": {"backgroundColor": EWS_COLOR["S"], 'color': EWS_COLOR["S"]}},
]

TABLES_CONTAINER = {'display': 'flex',"alignItems": "center",
                   "justifyContent": "center","flexDirection": "column"}

DATA_EXPORT_BUTTON = {
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
    }

DETAILS_GRID_MAIN_CONTAINER = {
    "display": "grid",
    "gap": "10px",  # Adds space between grid items
    "padding": "10px",  # Space around the edges of the grid
    "width": "100%",
    "height": "100vh",
}

DETAILS_GRID_CELLS = {
    "gridColumn": f"span 1", 
    "gridRow": f"span 1"
}

DETAILS_GRID_BUTTON = {
    "width": "100%",
    "height": "100%",
    "border": "1px solid #ddd",
    "textAlign": "center",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "fontSize": "18px",  # Increased text size
    "fontWeight": "bold",  # Optional: Make text bold
}
