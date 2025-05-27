"""
politimer base module.
"""

"""
App bootstrap module — instantiates model, controller, and views.
"""

import tkinter as tk
from politimer.model_timer import TimerModel  # Your actual model class from earlier sessions
from politimer.controller import TimerController
from politimer.view_gui import GuiView

def run(schedule_path: str):
    timer = TimerModel(schedule_path)
    root = tk.Tk()
    root.attributes("-fullscreen", True)

    controller = TimerController(timer, root)
    view = GuiView(root)
    controller.add_display(view)

    root.mainloop()
