"""Application entry point. Create App, wire services and start Tk mainloop.
Run with:
python -m accessible_tablet.app
"""

from typing import Dict, Optional
import tkinter as tk
from .menu import MainMenuPage
from .services.tts_service import TTSService
from .services.url_server import start_url_server


class App(tk.Tk):
    """Main application window / orchestrator."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Accessible Menu")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")
        self.current_frame: Optional[tk.Frame] = None
        self.frames: Dict[str, tk.Frame] = {}
        # services
        self.tts = TTSService()
        # start server
        start_url_server()
        # show main menu
        self.show_frame("main")
        # bind minimal keys (space / enter simple mapping)
        self.bind("<Return>", lambda e: self.select_current())


    def show_frame(self, key: str) -> None:
        """Create or show a named frame.
        For simplicity we create frames on demand. Keys: 'main', 'settings', ...
        """
        if self.current_frame:
            self.current_frame.pack_forget()
        if key == "main":
            frame = MainMenuPage(self)
            self.current_frame = frame
            frame.pack(expand=True, fill="both")
            # register for scanning
            self.frames[key] = frame
        else:
            # stub: other pages should be implemented similarly
            frame = MainMenuPage(self) # fallback
            self.current_frame = frame
            frame.pack(expand=True, fill="both")
            self.frames[key] = frame


    def select_current(self) -> None:
        """Invoke currently highlighted button (simplified: triggers first button)."""
        if not self.current_frame:
            return
        btns = getattr(self.current_frame, "buttons", [])
        if btns:
            btns[0].invoke()


    def shutdown(self) -> None:
        """Graceful shutdown: stop services and quit Tk."""
        try:
            self.tts.stop()
        finally:
            self.quit()



def main() -> None:
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        # Safeguard: only call shutdown if still alive
        if hasattr(app, "shutdown"):
            try:
                app.shutdown()
            except Exception:
                pass


# def main() -> None:
#     """
#     Run the app.
#     """
#     app = App()
#     try:
#         app.mainloop()
#     finally:
#         app.shutdown()


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
