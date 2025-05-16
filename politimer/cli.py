"""
CLI interface for politimer project.
"""

import sys
from politimer.gui import run_gui

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/schedule.json"
    run_gui(path)
