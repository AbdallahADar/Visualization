from dash import html, dcc

def create_main_layout():
    return html.Div([
        dcc.Store(id="state-manager"),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ], style={'backgroundColor': '#F5F5F5'})  # Adjust background color as needed
