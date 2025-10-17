"""Utility helpers extracted from original script.
Functions included are safe wrappers and small helpers to keep platform specifics isolated.
"""

from typing import Tuple, Optional
import platform

try:
    import win32gui # type: ignore
    import win32process # type: ignore
    import win32con # type: ignore
    import ctypes
    WINDOWS_AVAILABLE = True
except Exception as e: # pragma: no cover - Windows-only
    print("Error while importing, windows is not available")
    print(e)
    WINDOWS_AVAILABLE = False


def is_windows() -> bool:
    """Return True if the host OS is Windows."""
    return platform.system() == "Windows"


def get_active_window_name() -> Tuple[str, Optional[int]]:
    """Get the active window title and its PID if available.

    Returns
    -------
    title : str
    Active window title or empty string if unavailable.
    pid : Optional[int]
    PID of the window process if known.
    """
    if not WINDOWS_AVAILABLE:
        return "", None
    
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    name = win32gui.GetWindowText(hwnd)
    return name or "", pid


def minimize_terminal() -> None:
    """Minimize the console window on Windows, no-op otherwise."""
    if not WINDOWS_AVAILABLE:
        return
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    except Exception:
        pass
