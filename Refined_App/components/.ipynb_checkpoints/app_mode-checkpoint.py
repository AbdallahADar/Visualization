import dash
from dash import html
from utils.styles import SELECTION_CONTAINER, DEMO_SELECTION_HALF, DEMO_SELECTION_HEADER, DETAILS_SELECTION_HALF, DETAILS_SELECTION_HEADER
from utils.ids import APP_SELECTION_IDS

## Define container

app_mode = html.Div(
    id = APP_SELECTION_IDS["overall-container"],
    style = SELECTION_CONTAINER,
    children = [
        html.Div(
            id = APP_SELECTION_IDS["demo-block"],
            style = DEMO_SELECTION_HALF,
            children = html.H1("Demo App", style = DEMO_SELECTION_HEADER)
        ),
        html.Div(
            id = APP_SELECTION_IDS["details-block"],
            style = DETAILS_SELECTION_HALF,
            children = html.H1("Model Details", style = DETAILS_SELECTION_HEADER)
        )
    ]
)