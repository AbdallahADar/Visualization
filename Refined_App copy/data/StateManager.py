from plots.placeholder import PLACEHOLDER

## Define State manager class

class StateManager:

    # Initialize State
    def __init__(self):
        self.step = ""
        self.country = ""
        self.us_state = ""
        self.us_county = ""
        self.nuts1 = ""
        self.nuts2 = ""
        self.nuts3 = ""
        self.map_sector = "All"
        self.risk_type = "Overall Risk"
        self.geo_fig = PLACEHOLDER
        self.tree_fig = PLACEHOLDER
        self.selected_rows = []

    # To dict function defined
    def to_dict(self):
        return {k:v for k,v in self.__dict__.items()}

    # From dict function
    @classmethod
    def from_dict(cls, data):
        # Create an instance from a dictionary, handling any complex types if needed
        instance = cls()
        instance.__dict__.update(data)
        return instance 