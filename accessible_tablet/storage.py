"""Persistent storage helpers (load/save JSON) with simple validation.
This module isolates reading/writing last_watched.json and loading tables.
"""

from typing import Any, Dict
import json
import os
from . import config


def load_last_watched() -> Dict[str, Any]:
    """Load last watched positions from JSON file.
    
    Returns
    -------
    dict
    Mapping of show title to url or position object.
    """
    try:
        if os.path.exists(config.LAST_WATCHED_FILE):
            with open(config.LAST_WATCHED_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception:
        return {}
    return {}


def save_last_watched(data: Dict[str, Any]) -> None:
    """Persist last watched mapping to disk (creates parent dir if needed)."""
    os.makedirs(os.path.dirname(config.LAST_WATCHED_FILE), exist_ok=True)
    with open(config.LAST_WATCHED_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
