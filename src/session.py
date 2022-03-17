import json
from utils import Utilities


class Session:
    def __init__(self):
        self.race_counts = 0
        self.wins = 0
        self.losses = 0
        self.universe = None
        self.result = None  # Can either be "Success" or "Error"

    def save_session(self):
        file_location = "data/sessions.json"
