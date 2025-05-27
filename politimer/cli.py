"""
CLI interface for politimer project.
"""

import sys
from politimer.base import run  # formerly run_gui

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/schedule.json"
    run(path)
