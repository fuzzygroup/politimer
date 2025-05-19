import sys
import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
from PIL import Image,ImageDraw,ImageFont


class Eink:
    def __init__(self):
        # Setup paths
        self.picdir = picdir
        self.font = ImageFont.truetype(os.path.join(self.picdir, 'Font.ttc'), 48)

        # Initialize display
        self.epd = epd2in13_V4.EPD()
        logging.info("Initializing e-ink display...")
        self.epd.init()
        self.epd.Clear()

        # Create a blank image for drawing
        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.image)

        # State tracking
        self.current_speaker = ""
        self.full_refresh_needed = True
        self.refresh_counter = 0
        self.force_refresh_every = 10  # Force full refresh every 10 updates

    def update_time(self, display_text: str):
        """
        Update the display with the speaker name and time.
        Will use full refresh when speaker changes or periodically.
        """
        # Parse the text (expected format: "SpeakerName\n00:00")
        parts = display_text.split('\n')
        speaker = parts[0] if len(parts) > 0 else ""
        time_str = parts[1] if len(parts) > 1 else ""

        # Determine if we need a full refresh
        speaker_changed = (speaker != self.current_speaker)
        if speaker_changed:
            self.full_refresh_needed = True
            self.current_speaker = speaker

        # Increment counter and check if we need periodic full refresh
        self.refresh_counter += 1
        if self.refresh_counter >= self.force_refresh_every:
            self.full_refresh_needed = True
            self.refresh_counter = 0

        # Clear the image and redraw everything
        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.image)

        # Draw the speaker name and time
        self.draw.text((20, 10), speaker, font=self.font, fill=0)
        self.draw.text((20, 80), time_str, font=self.font, fill=0)

        # Choose update method based on state
        if self.full_refresh_needed:
            logging.info("Full display refresh")
            self.epd.display(self.epd.getbuffer(self.image))
            self.full_refresh_needed = False
        else:
            logging.info("Partial display update")
            self.epd.displayPartial(self.epd.getbuffer(self.image))

    def clear(self):
        """Clear the e-ink display."""
        self.epd.Clear()
        self.full_refresh_needed = False
        self.refresh_counter = 0

    def sleep(self):
        """Put the display to sleep to save power."""
        self.epd.sleep()
