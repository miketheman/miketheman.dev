#!/usr/bin/env python3
"""Render dist/ and write pinned PNG screenshots for PR visual diffs.

Captures both desktop and mobile viewports. Mobile uses is_mobile=True +
has_touch=True so the responsive `<picture>` element falls through to the
QR avatar (hover-fine media query doesn't match).

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
OUT_DIR = Path("assets/snapshots")

# CSS selectors whose content changes every build — painted as solid rectangles.
MASK_SELECTORS = [".footer"]

CAPTURES = [
    ("homepage.png", {
        "viewport": {"width": 800, "height": 1400},
        "device_scale_factor": 2,
    }),
    ("homepage-mobile.png", {
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    }),
]


def main():
    dist_path = Path(DIST)
    if not (dist_path / "index.html").exists():
        raise SystemExit(f"❌ {DIST}/index.html not found. Run `just build` first.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name, opts in CAPTURES:
                out = OUT_DIR / name
                page = browser.new_page(**opts)
                page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
                page.screenshot(
                    path=out,
                    full_page=True,
                    mask=[page.locator(sel) for sel in MASK_SELECTORS],
                )
                page.close()
                print(f"📸 wrote {out}")
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
