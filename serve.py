#!/usr/bin/env python3
"""Serve the wedding site locally, including wedding.json."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8001"))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    print(f"Wedding site available at http://{HOST}:{PORT}/ (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping wedding site server.")
    finally:
        server.server_close()
