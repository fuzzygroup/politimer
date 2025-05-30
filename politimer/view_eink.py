import threading
import queue

import sys
import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import textwrap
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont

class EinkView:
    def __init__(self):
        # Setup paths
        self.picdir = picdir
        self.font = ImageFont.truetype(os.path.join(self.picdir, 'Font.ttc'), 64)

        self.epd = epd7in5_V2.EPD()
        logging.info("Initializing e-ink display...")
        self.epd.init()
        self.epd.Clear()

        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.image)

        self.current_speaker = ""
        self.full_refresh_needed = True

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

        self.image = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.draw = ImageDraw.Draw(self.image)
        module_dir = os.path.dirname(__file__)
        logo_path = os.path.join(module_dir, "../data/logo.png")
        logo_size = 400
        try:
            logo = Image.open(logo_path).convert('1')
            logo = logo.resize((logo_size, logo_size), resample=Image.Resampling.LANCZOS)
            self.image.paste(logo, (20, int((self.epd.height - logo_size) / 2)))
        except Exception as e:
            logging.warning(f"Logo not loaded: {e}")

        text_x = 500
        base_y = 160
        line_spacing = 60

        if " " in speaker:
            wrapped_lines = textwrap.wrap(speaker, width=12)
        else:
            wrapped_lines = [speaker]

        for i, line in enumerate(wrapped_lines):
            y = base_y + i * line_spacing
            self.draw.text((text_x, y), line, font=self.font, fill=0)

        time_y = base_y + len(wrapped_lines) * line_spacing + 10
        self.draw.text((text_x, time_y), time_str, font=self.font, fill=0)
    
        if self.full_refresh_needed:
            logging.info("Full display refresh")
            self.epd.display(self.epd.getbuffer(self.image))
            self.full_refresh_needed = False
        else:
            logging.info("Partial display update")
            self.epd.init_part()
            self.epd.display_Partial(self.epd.getbuffer(self.image), 0, 0, self.epd.width, self.epd.height)

    def clear(self):
        self.epd.Clear()
        self.full_refresh_needed = False
        self.refresh_counter = 0

    def sleep(self):
        self.epd.sleep()
