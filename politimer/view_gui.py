import os
import tkinter as tk
from tkinter import PhotoImage

class GuiView:
    def __init__(self, root):
        self.controller = None
        self.root = root

        # Internal state for display
        self.speaker = ""
        self.remaining_seconds = 0
        self.flash = False
        self.flash_state = True

        # GUI setup
        root.configure(bg="white")
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Logo display
        self.logo_frame = tk.Frame(self.main_frame, bg="white")
        self.logo_frame.pack(side="left", padx=20, pady=20)
        module_dir = os.path.dirname(__file__)
        logo_path = os.path.join(module_dir, "../data/logo.png")
        self.image = PhotoImage(file=logo_path)
        self.image_label = tk.Label(self.logo_frame, image=self.image, bg="white")
        self.image_label.pack(padx=10, pady=10)

        # Timer label
        self.timer_frame = tk.Frame(self.main_frame, bg="white")
        self.timer_frame.pack(side="left", expand=True, fill=tk.BOTH)
        self.label = tk.Label(self.timer_frame, text="", font=("Helvetica", 200), fg="black", bg="white")
        self.label.pack(expand=True, fill=tk.BOTH)

        self.tick()  # Start the ticking visual loop

    def set_controller(self, controller):
        self.controller = controller

    def update(self, speaker, time_str, is_expired):
        self.speaker = speaker
        self.remaining_seconds = self._parse_time_str(time_str)
        self.flash = is_expired
        self.update_display()

    def _parse_time_str(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds

    def update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_display = f"{minutes:02}:{seconds:02}"

        if self.flash:
            color = "red" if self.flash_state else "black"
            self.label.config(fg=color)
            self.flash_state = not self.flash_state
        else:
            self.label.config(fg="black")

        self.label.config(text=f"{self.speaker}\n{time_display}")

    def tick(self):
        # View doesn't manage state, but continues flashing if needed
        if self.flash and self.remaining_seconds == 0:
            self.update_display()

        self.root.after(1000, self.tick)
