"""Application configuration constants.
"""
from typing import Final
import os


DATA_DIR: Final[str] = os.path.join(os.path.dirname(__file__), "..", "data")
LAST_WATCHED_FILE: Final[str] = os.path.join(os.path.dirname(__file__), "..",
                                             "data", "last_watched.json")
CONTROL_BAR_PATH: Final[str] = os.path.join(os.path.dirname(__file__), "utils", "control_bar.py")
EPISODE_SHEET_NAME: Final[str] = "EPISODE_SELECTION.xlsx"
