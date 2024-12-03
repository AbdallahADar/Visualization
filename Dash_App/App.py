from dash import Dash, dcc, html
from components.layout import create_main_layout
from components.callbacks import register_callbacks

# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Set the layout
app.layout = create_main_layout()

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
