import dash
from dash import html
import dash_bootstrap_components as dbc
from utils.styles import DETAILS_GRID_MAIN_CONTAINER, DETAILS_GRID_CELLS, DETAILS_GRID_BUTTON
from utils.constants import TOTAL_CELLS, NUM_ROWS, NUM_COLS, GRID_CELLS
from utils.ids import DETAILS_GRID_IDS, DETAILS_POP_UP_IDS

## Define container

details_grid = html.Div(
    id = DETAILS_GRID_IDS["overall-container"],
    style = {'display':'hidden'},
    children = [
        html.Div(
            style = {
                **DETAILS_GRID_MAIN_CONTAINER,
                "gridTemplateColumns": f"repeat({NUM_COLS}, 1fr)",  # Number of columns
                "gridTemplateRows": f"repeat({NUM_ROWS}, 1fr)",  # Number of rows
            },
            children = [
                html.Div(
                    style = DETAILS_GRID_CELLS,
                    children = [
                        dbc.Button(
                            GRID_CELLS[i],
                            id = DETAILS_GRID_IDS[f"G{i+1}"],
                            disabled = True if GRID_CELLS[i] == "Coming Soon" else False,
                            style = {
                                **DETAILS_GRID_BUTTON,
                                "backgroundColor": "#999999" if GRID_CELLS[i] == "Coming Soon" else "#007bff",
                                "color": "black" if GRID_CELLS[i] != "Coming Soon" else  "white",
                                "cursor": "pointer" if GRID_CELLS[i] != "Coming Soon" else  "not-allowed",
                            }
                        )
                    ]
                ) for i in range(TOTAL_CELLS)
            ]
        ),
        # Modal for pop-ups
        dbc.Modal(
            id = DETAILS_POP_UP_IDS["overall-container"],
            is_open = False,
            size = "lg",
            children = [
                dbc.ModalHeader(),
                dbc.ModalBody(
                    id = DETAILS_POP_UP_IDS["body"],
                    children = "Content for the clicked feature."
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id = DETAILS_POP_UP_IDS["button"], n_clicks=0, color="secondary")
                )
            ]
        )
    ],
)