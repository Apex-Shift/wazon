# core/engine.py

class BaseWazonModule:
    def __init__(self):
        self.name = "Base Module"
        self.category = "general"
        self.description = "No description provided."
        self.options = {}

    def set_option(self, key, value):
        if key in self.options:
            self.options[key]["value"] = value
        else:
            raise KeyError(f"Option '{key}' does not exist for this module.")

    async def execute(self, target):
        raise NotImplementedError("The execute method must be implemented by the module.")