# politimer/gui.py

import tkinter as tk
from politimer.base import Timer


class TimerApp:
    def __init__(self, root, timer: Timer):
        self.timer = timer
        self.root = root

        self.label = tk.Label(root, text="", font=("Helvetica", 72), fg="white", bg="black")
        self.label.pack(expand=True, fill=tk.BOTH)

        self.paused = True
        self.flash = False
        self.flash_state = True  # Whether text is visible
        self.remaining_seconds = self.timer.get_time()

        # Key bindings
        root.bind("<Left>", self.prev)
        root.bind("<Right>", self.next)
        root.bind("<space>", self.toggle_pause)
        root.bind("q", lambda e: root.quit())

        root.configure(bg="black")
        self.update_display()
        self.tick()

    def update_display(self):
        speaker = self.timer.get_speaker()
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_display = f"{minutes:02}:{seconds:02}"

        if self.flash:
            color = "red" if self.flash_state else "black"
            self.label.config(fg=color)
            self.flash_state = not self.flash_state
        else:
            self.label.config(fg="white")

        self.label.config(text=f"{speaker}\n{time_display}")

    def tick(self):
        if not self.paused and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        elif self.remaining_seconds == 0:
            self.flash = True

        self.update_display()
        self.root.after(1000, self.tick)

    def next(self, event=None):
        self.timer.next_setting()
        self.remaining_seconds = self.timer.get_time()
        self.flash = False
        self.paused = True
        self.update_display()

    def prev(self, event=None):
        self.timer.prev_setting()
        self.remaining_seconds = self.timer.get_time()
        self.flash = False
        self.paused = True
        self.update_display()

    def toggle_pause(self, event=None):
        self.paused = not self.paused

def run_gui(schedule_path):
    timer = Timer(schedule_path)
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # Optional: makes it kiosk mode
    app = TimerApp(root, timer)
    root.mainloop()
