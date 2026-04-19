#!/usr/bin/env python3
"""Render dist/ and write a pinned PNG screenshot for PR visual diffs.

Volatile regions (e.g. "Updated <date>") are masked so they don't drive
false-positive diffs between PRs.
"""
import functools
import http.server
import socketserver
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 8765
DIST = "dist"
OUT = Path("assets/snapshots/homepage.png")

# CSS selectors whose content changes every build — painted as solid rectangles.
MASK_SELECTORS = [".footer"]


def main():
    dist_path = Path(DIST)
    if not (dist_path / "index.html").exists():
        raise SystemExit(f"❌ {DIST}/index.html not found. Run `just build` first.")

    OUT.parent.mkdir(parents=True, exist_ok=True)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(
                viewport={"width": 800, "height": 1400},
                device_scale_factor=2,
            )
            page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
            page.screenshot(
                path=OUT,
                full_page=True,
                mask=[page.locator(sel) for sel in MASK_SELECTORS],
            )
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    print(f"📸 wrote {OUT}")


if __name__ == "__main__":
    main()
