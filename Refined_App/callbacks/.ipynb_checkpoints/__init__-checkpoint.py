from .search_selection import register_callbacks as search_selection
from .sector_dropdown import register_callbacks as sector_drop_down
from .geo_selection import register_callbacks as geo_selection
from .sector_ndy_selection import register_callbacks as sector_ndy_selection


def register_all_callbacks(app):
    """
    Register all callbacks with the app.
    """
    search_selection(app)
    sector_drop_down(app)
    geo_selection(app)
    sector_ndy_selection(app)
