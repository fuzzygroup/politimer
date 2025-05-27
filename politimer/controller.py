class TimerController:
    def __init__(self, timer_model, root):
        self.model = timer_model
        self.root = root
        self.displays = []
        self.model.add_observer(self)
        self.start_tick_loop()  # start ticking
        self.bind_keys()

    def bind_keys(self):
        self.root.bind("a", self.handle_prev)
        self.root.bind("c", self.handle_next)
        self.root.bind("b", self.handle_toggle_pause)

        self.root.bind("q", self.quit_app)

    def add_display(self, display):
        self.displays.append(display)
        display.set_controller(self)

    def update_displays(self):
        time_remaining = self.model.get_remaining_seconds()
        speaker = self.model.get_speaker()
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        time_str = f"{minutes:02}:{seconds:02}"

        for display in self.displays:
            display.update(speaker, time_str, self.model.is_expired())

    def tick(self):
        self.update_displays()

    # Public event handlers (for keybindings)
    def handle_next(self, event=None):
        self._next()

    def handle_prev(self, event=None):
        self._prev()

    def handle_toggle_pause(self, event=None):
        self._toggle_pause()

    def quit_app(self, event=None):
        self.root.quit()

    # Internal logic methods (call these from other code, like the view)
    def _next(self):
        self.model.reset_timer()
        self.model.next_setting()
        self.update_displays()

    def _prev(self):
        self.model.reset_timer()
        self.model.prev_setting()
        self.update_displays()


    def _toggle_pause(self):
        print("Toggling pause...")
        if self.is_running():
            print("Pausing")
            self.model.pause_timer()
        else:
            print("Starting")
            self.model.start_timer()

    def start_tick_loop(self):
        self.tick()  # update displays
        self.root.after(1000, self.start_tick_loop)  # call again in 1 second


    def is_running(self):
        return self.model.start_time is not None and self.model.paused_time is None
