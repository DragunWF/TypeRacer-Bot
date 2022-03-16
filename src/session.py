import json
from utils import Utilities


class Session:
    def __init__(self):
        self.race_counts = 0
        self.universe = "Main"  # Default for now
        self.result = None  # Can either be "Success" or "Error"

    def save_session(self):
        pass
