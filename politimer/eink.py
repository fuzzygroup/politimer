import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13b_V4
import time
from PIL import Image,ImageDraw,ImageFont


class Eink:
    def __init__(self):
        # Setup paths
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.picdir = os.path.join(base_dir, 'pic')
        self.font = ImageFont.truetype(os.path.join(self.picdir, 'Font.ttc'), 24)

        # Initialize display
        self.epd = epd2in13b_V4.EPD()
        logging.info("Initializing e-ink display...")
        self.epd.init()
        self.epd.Clear()

        # Create a blank image for drawing
        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.image)

    def update_time(self, current_time_str: str):
        """Update the display with a new time string (e.g., '00:05:00')."""
        self.draw.rectangle((120, 80, 220, 105), fill=255)  # Clear the area
        self.draw.text((120, 80), current_time_str, font=self.font, fill=0)
        self.epd.displayPartial(self.epd.getbuffer(self.image))

    def clear(self):
        """Clear the e-ink display."""
        self.epd.Clear()

    def sleep(self):
        """Put the display to sleep to save power."""
        self.epd.sleep()
