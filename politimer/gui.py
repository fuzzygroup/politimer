# politimer/gui.py

import tkinter as tk
from tkinter import PhotoImage
from politimer.base import Timer
from politimer.eink import Eink

class TimerApp:
    def __init__(self, root, timer: Timer):
        self.timer = timer
        self.root = root

        # Configure the root window
        root.configure(bg="white")

        # Create top frame for logo
        self.top_frame = tk.Frame(root, bg="white")
        self.top_frame.pack(side="top", fill="x")

        # Add the logo image
        self.image = PhotoImage(file="/home/timeruser/politimer/data/logo.png")
        self.image_label = tk.Label(self.top_frame, image=self.image, bg="white")
        self.image_label.pack(side="left", padx=10, pady=10)

        # Create a separate frame for the timer display
        self.timer_frame = tk.Frame(root, bg="white")
        self.timer_frame.pack(expand=True, fill=tk.BOTH)

        # Add the timer label to the timer frame
        self.label = tk.Label(self.timer_frame, text="", font=("Helvetica", 256), fg="black", bg="white")
        self.label.pack(expand=True, fill=tk.BOTH)

        # Initialize timer states
        self.paused = True
        self.flash = False
        self.flash_state = True  # Whether text is visible
        self.remaining_seconds = self.timer.get_time()

        # Key bindings
        root.bind("a", self.prev)
        root.bind("c", self.next)
        root.bind("b", self.toggle_pause)
        root.bind("q", lambda e: root.quit())

        # Initialize E-ink display (commented out)
        # self.eink_display = Eink()

        # Start the timer display
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
            self.label.config(fg="black")  # Changed from "white" to "black" for visibility

        self.label.config(text=f"{speaker}\n{time_display}")
        # self.eink_display.update_time(f"{speaker}\n{time_display}")

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
