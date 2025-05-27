import json
import time
from datetime import timedelta
from typing import Optional


class TimerModel:
    def __init__(self, schedule_path: str):
        self.schedule = self.load_schedule(schedule_path)
        self.index = 0  # current speaker index
        self.duration = 0  # seconds
        self.start_time: Optional[float] = None  # monotonic start time
        self.paused_time: Optional[float] = None
        self.expired = False
        self.observers = []

        self.reset_timer()

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
        return self.schedule[self.index].get("speaker", "")

    def next_setting(self):
        if self.index < len(self.schedule) - 1:
            self.index += 1
            self.reset_timer()
            self.notify_observers("schedule_changed")

    def prev_setting(self):
        if self.index > 0:
            self.index -= 1
            self.reset_timer()
            self.notify_observers("schedule_changed")

    def set_time(self, new_time):
        self.schedule[self.index]["time"] = new_time
        self.reset_timer()
        self.notify_observers("time_changed")

    # Observer pattern methods
    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event_type):
        for observer in self.observers:
            if hasattr(observer, 'model_updated'):
                observer.model_updated(self, event_type)

    def reset_timer(self):
        self.duration = self.get_time()
        self.start_time = None
        self.paused_time = None
        self.expired = False
        self.notify_observers("timer_reset")

    def start_timer(self):
        if self.paused_time is not None and self.start_time is not None:
            # Resuming from pause
            pause_duration = time.monotonic() - self.paused_time
            self.start_time = self.start_time + pause_duration
            self.paused_time = None
        else:
            self.start_time = time.monotonic()
        self.notify_observers("timer_started")

    def pause_timer(self):
        if self.start_time is not None:
            self.paused_time = time.monotonic()
            self.notify_observers("timer_paused")

    def is_expired(self):
        return self.get_remaining_seconds() <= 0

    def get_remaining_seconds(self):
        if self.start_time is None:
            return self.duration
        if self.paused_time is not None:
            elapsed = self.paused_time - self.start_time
        else:
            elapsed = time.monotonic() - self.start_time
        remaining = self.duration - elapsed
        if remaining <= 0:
            self.expired = True
            return 0
        return int(remaining)
