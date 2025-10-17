"""Small HTTP server to accept URL save callbacks.
This is a reimplementation of the minimal URLSaveHandler from the original script.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import threading
from ..menu import MenuFrame
from ..storage import load_last_watched, save_last_watched


ALLOWED_DOMAINS = {
    "youtube.com",
    "netflix.com",
    "pluto.tv",
    "primevideo.com",
    "disneyplus.com",
    }




class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None: # pragma: no cover - simple server
        """
        TODO
        """
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        url = qs.get("url", [None])[0]
        show = getattr(MenuFrame, "active_show", None)

        if not show or not url:
            self.send_response(204)
            self.end_headers()
            return

        host = urllib.parse.urlparse(url).netloc.lower()
        if not any(domain in host for domain in ALLOWED_DOMAINS):
            self.send_response(204)
            self.end_headers()
            return

        data = load_last_watched()
        data[show] = url
        save_last_watched(data)
        self.send_response(204)
        self.end_headers()


def start_url_server(host: str = "127.0.0.1", port: int = 8765) -> None:
    """
    TODO

    Parameters
    ----------
    host : str, optional
        _description_, by default "127.0.0.1"
    port : int, optional
        _description_, by default 8765
    """
    server = HTTPServer((host, port), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
