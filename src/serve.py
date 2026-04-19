#!/usr/bin/env python3
"""
Simple development server for testing the generated site locally.
"""
import functools
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000
DIRECTORY = "dist"


def main():
    dist_path = Path(DIRECTORY)
    if not dist_path.exists():
        print(f"❌ {DIRECTORY} directory not found. Run `just build` first.")
        return

    if not (dist_path / "index.html").exists():
        print(f"❌ index.html not found in {DIRECTORY}. Run `just build` first.")
        return

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🚀 Serving at {url}")
        print("Press Ctrl+C to stop the server")

        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    main()