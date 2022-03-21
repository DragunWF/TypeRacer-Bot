import json
from pathlib import Path


class Session:
    def __init__(self):
        self.races = 0
        self.wins = 0
        self.losses = 0
        self.universe = None
        self.result = None
        self.registered = None
        self.practice_mode = None

    def validate_information(self):
        if self.practice_mode:
            self.wins = None
            self.losses = None

    def save_session(self):
        self.validate_information()

        result = "success" if self.result else "interrupted"
        data = json.loads(Path("data/sessions.json").read_text())
        session_data = {"registered": self.registered, "practice_mode": self.practice_mode,
                        "races": self.races, "wins": self.wins, "losses": self.losses,
                        "universe": self.universe, "session_result": result}
        data.append(session_data)

        formatted = json.dumps(data, sort_keys=False, indent=2, separators=(',', ': '))
        Path("data/sessions.json").write_text(formatted)
