import threading
import queue

import sys
import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
from PIL import Image,ImageDraw,ImageFont

class EinkView:
    def __init__(self):
        # Setup paths
        self.picdir = picdir
        self.font = ImageFont.truetype(os.path.join(self.picdir, 'Font.ttc'), 48)

        self.epd = epd2in13_V4.EPD()
        logging.info("Initializing e-ink display...")
        self.epd.init()
        self.epd.Clear()

        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.image)

        self.current_speaker = ""
        self.full_refresh_needed = True
        self.refresh_counter = 0
        self.force_refresh_every = 10

        self.controller = None
        self.update_queue = queue.Queue()

        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def set_controller(self, controller):
        self.controller = controller

    def update(self, speaker, time_str, is_expired):
        display_text = f"{speaker}\n{time_str}"
        self.update_queue.put(display_text)

    def _worker(self):
        while True:
            try:
                display_text = self.update_queue.get()
                self._handle_update(display_text)
            except Exception as e:
                logging.exception("Eink update failed")

    def _handle_update(self, display_text):
        parts = display_text.split('\n')
        speaker = parts[0] if len(parts) > 0 else ""
        time_str = parts[1] if len(parts) > 1 else ""

        speaker_changed = (speaker != self.current_speaker)
        if speaker_changed:
            self.full_refresh_needed = True
            self.current_speaker = speaker

        self.refresh_counter += 1
        if self.refresh_counter >= self.force_refresh_every:
            self.full_refresh_needed = True
            self.refresh_counter = 0

        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.image)

        self.draw.text((20, 10), speaker, font=self.font, fill=0)
        self.draw.text((20, 70), time_str, font=self.font, fill=0)

        if self.full_refresh_needed:
            logging.info("Full display refresh")
            self.epd.display(self.epd.getbuffer(self.image))
            self.full_refresh_needed = False
        else:
            logging.info("Partial display update")
            self.epd.displayPartial(self.epd.getbuffer(self.image))

    def clear(self):
        self.epd.Clear()
        self.full_refresh_needed = False
        self.refresh_counter = 0

    def sleep(self):
        self.epd.sleep()
