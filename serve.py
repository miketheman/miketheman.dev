#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""
Simple development server for testing the generated site locally.
"""
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000
DIRECTORY = "dist"

def main():
    # Ensure dist directory exists
    dist_path = Path(DIRECTORY)
    if not dist_path.exists():
        print(f"❌ {DIRECTORY} directory not found. Run ./generate.py first.")
        return
    
    if not (dist_path / "index.html").exists():
        print(f"❌ index.html not found in {DIRECTORY}. Run ./generate.py first.")
        return

    # Change to dist directory
    import os
    os.chdir(DIRECTORY)
    
    # Start server
    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🚀 Serving at {url}")
        print("Press Ctrl+C to stop the server")
        
        # Open browser
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    main()