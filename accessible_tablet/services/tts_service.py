"""Simple text-to-speech service wrapper.


Provides a background queue to avoid blocking UI.
"""
from typing import Optional
import queue
import threading

try:
    from pyttsx3 import init # type: ignore
    AVAILABLE = True
except Exception: # pragma: no cover - optional dependency
    AVAILABLE = False




class TTSService:
    """Background TTS service.


    Parameters
    ----------
    _engine : object
    Underlying engine instance (pyttsx3 engine when available).
    """


    def __init__(self) -> None:
        self._queue: "queue.Queue[Optional[str]]" = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._engine = init() if AVAILABLE else None
        self._start_worker()


    def _start_worker(self) -> None:
        def _worker() -> None:
            while True:
                text = self._queue.get()
                if text is None:
                    break
                if self._engine:
                    try:
                        self._engine.say(text)
                        self._engine.runAndWait()
                    except Exception:
                        pass
                self._queue.task_done()

        self._thread = threading.Thread(target=_worker, daemon=True)
        self._thread.start()


    def speak(self, text: str) -> None:
        """Enqueue a text to be spoken. Clears the queue if one item exists.


        Parameters
        ----------
        text : str
        The text to speak.
        """
        # Keep only the most recent utterance
        if self._queue.qsize() >= 1:
            with self._queue.mutex:
                self._queue.queue.clear()
                self._queue.put(text)


    def stop(self) -> None:
        """Graceful stop of the TTS thread."""
        try:
            self._queue.put(None)
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=1.0)
        except Exception:
            pass
