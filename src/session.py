import json
from pathlib import Path


class Session:
    def __init__(self):
        self.races = 0
        self.wins = 0
        self.losses = 0
        self.universe = None
        self.result = None

    def save_session(self):
        result = "success" if self.result else "interrupted"
        data = json.loads(Path("data/sessions.json").read_text())
        session_data = {"races": self.races,
                        "wins": self.wins, "losses": self.losses,
                        "universe": self.universe, "session_result": result}
        data.append(session_data)

        formatted = json.dumps(data, sort_keys=False,
                               indent=2, separators=(',', ': '))
        Path("data/sessions.json").write_text(formatted)
