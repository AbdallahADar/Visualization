class StateManager:
    def __init__(self):
        self.mode = "Sales"
        self.selected_status = {}
        self.page = 0
        self.step = "startPage"
        # Initialize other state variables...

    # Add methods for state management as required...
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.__dict__.update(data)
        return instance
