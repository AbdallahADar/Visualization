from .search_selection import register_callbacks as search_selection
from .sector_dropdown import register_callbacks as sector_dropdown
from .risk_type_dropdown import register_callbacks as risk_type_dropdown
from .geo_selection import register_callbacks as geo_selection
from .sector_ndy_selection import register_callbacks as sector_ndy_selection
from .row_selection import register_callbacks as row_selection
from .export_data import register_callbacks as export_data



def register_all_callbacks(app):
    """
    Register all callbacks with the app.
    """
    search_selection(app)
    geo_selection(app)
    sector_dropdown(app)
    risk_type_dropdown(app)
    sector_ndy_selection(app)
    row_selection(app)
    export_data(app)