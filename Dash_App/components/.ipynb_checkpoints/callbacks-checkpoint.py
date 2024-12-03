from dash import Input, Output, html
from pages.exploratory_page import layout as exploratory_layout
from pages.targeted_page import layout as targeted_layout
from pages.geo_page import layout as geo_layout

def register_callbacks(app):
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/exploratory':
            return exploratory_layout()
        elif pathname == '/targeted':
            return targeted_layout()
        elif pathname == '/geo':
            return geo_layout()
        else:
            return html.H1("404: Page not found")
