"""
politimer base module.
"""
import json
from datetime import timedelta

class Timer:
    def __init__(self, schedule_path: str):
        self.schedule = self.load_schedule(schedule_path)
        self.index = 0  # current speaker index

    def load_schedule(self, path: str):
        with open(path, 'r') as f:
            return json.load(f)

    def get_time(self):
        """Returns time in seconds from HH:MM:SS string."""
        time_str = self.schedule[self.index].get("time", "00:00:00")
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            td = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            return int(td.total_seconds())
        except ValueError:
            return 0  # fallback on bad format

    def get_speaker(self):
        return self.schedule[self.index].get("speaker")

    def display_time(self):
        # placeholder — will later connect to GUI
        print(f"{self.get_speaker()}: {self.get_time()}")

    def next_setting(self):
        if self.index < len(self.schedule) - 1:
            self.index += 1

    def prev_setting(self):
        if self.index > 0:
            self.index -= 1

    def set_time(self, new_time):
        self.schedule[self.index]["time"] = new_time
