"""Tkinter based menu frames extracted and redesigned into classes.

Only a subset of pages are provided (MainMenuPage, MenuFrame).
The goal is to provide a clean OO layout and preserve behaviors.
"""

from typing import Callable, List, Tuple
import tkinter as tk


class MenuFrame(tk.Frame):
    """Base frame for menu pages.

    Parameters
    ----------
    parent : Tk
    Parent application instance.
    title : str
    Title displayed at the top of the frame.
    """

    active_show: str = ""

    def __init__(self, parent: tk.Tk, title: str) -> None:
        super().__init__(parent, bg="black")
        self.parent = parent
        self.title = title
        self.buttons: List[tk.Button] = []
        self.title_label = tk.Label(self, text=self.title,
                                    font=("Arial", 36), bg="black", fg="white")
        self.title_label.pack(pady=20)


    def create_button_grid(self, items: List[Tuple[str, Callable[[],
                            None], str]], columns: int = 3) -> None:
        """
        Create the grid.
        #TODO complete the doc

        Parameters
        ----------
        items : List[Tuple[str, Callable[[], None], str]]
            _description_
        columns : int, optional
            _description_, by default 3
        """
        grid = tk.Frame(self, bg="black")
        grid.pack(expand=True, fill="both", padx=10, pady=10)
        self.buttons = []
        for i, (text, cmd, speak_text) in enumerate(items):
            r, c = divmod(i, columns)
            btn = tk.Button(grid, text=text, font=("Arial Black", 36), bg="light blue", fg="black",
            command=lambda c=cmd, s=speak_text: self._on_select(c, s), wraplength=700)
            btn.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            self.buttons.append(btn)
        # configure grid weights
        rows = (len(items) + columns - 1) // columns
        for rr in range(rows):
            grid.rowconfigure(rr, weight=1)
        for cc in range(columns):
            grid.columnconfigure(cc, weight=1)


    def _on_select(self, cmd: Callable[[], None], speak_text: str) -> None:
        cmd()
        if speak_text and getattr(self.parent, "tts", None):
            self.parent.tts.speak(speak_text)




class MainMenuPage(MenuFrame):
    """Main application menu with 4 actions."""

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent, "Main Menu")
        buttons = [
        ("Emergency", self._emergency, "Emergency"),
        ("Settings", lambda: parent.show_frame("settings"), "Settings"),
        ("Communication", lambda: parent.show_frame("communication"), "Communication"),
        ("Entertainment", lambda: parent.show_frame("entertainment"), "Entertainment"),
        ]
        self.create_button_grid(buttons, columns=2)


    def _emergency(self) -> None:
        # simple emergency: announce and no blocking
        if getattr(self.parent, "tts", None):
            self.parent.tts.speak("Help, help, help")
