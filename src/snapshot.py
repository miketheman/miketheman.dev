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
import os
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 8765
DIST = "dist"
OUT_DIR = Path("assets/snapshots")

# CSS selectors whose content changes every build — painted as solid rectangles.
MASK_SELECTORS = [".footer"]

# The margin specimens are picked with Math.random() on every visit, which would
# make every capture a different pair of herbs and every PR a false diff. Pin the
# source of the randomness rather than the outcome, so the real selection code
# still runs and a bug in it still shows up in the baseline.
PIN_RANDOM = "Math.random = function () { return 0.5; };"

CAPTURES = [
    ("homepage.png", {
        "viewport": {"width": 800, "height": 1400},
        "device_scale_factor": 2,
    }),
    # Above the 56rem breakpoint, where the specimens move out of the column and
    # into the real margin. Neither existing capture is wide enough to show it.
    ("homepage-wide.png", {
        "viewport": {"width": 1280, "height": 900},
        "device_scale_factor": 2,
    }),
    ("homepage-mobile.png", {
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    }),
]

# The real page carries too few extras for `expandable_extras` to be non-empty,
# so the <details> expander — its label swap, hit target and open layout — never
# renders and never gets reviewed. Rebuild with a lower threshold and capture it
# open, so the component is exercised before a sixth extra ships it live.
EXPANDER_CAPTURE = ("homepage-expander.png", {
    "viewport": {"width": 390, "height": 844},
    "device_scale_factor": 2,
    "is_mobile": True,
    "has_touch": True,
})


def main():
    dist_path = Path(DIST)
    if not (dist_path / "index.html").exists():
        raise SystemExit(f"❌ {DIST}/index.html not found. Run `just build` first.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    # Without this, the socket sits in TIME_WAIT after a run and the next
    # `just snapshot` within the minute dies on "Address already in use".
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    def capture(browser, name, opts, open_expander=False):
        out = OUT_DIR / name
        page = browser.new_page(**opts)
        page.add_init_script(PIN_RANDOM)
        page.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
        if open_expander:
            summary = page.locator(".extras-summary")
            summary.wait_for(state="visible", timeout=5000)
            summary.click()
            page.wait_for_selector(".extras-details[open]")
        page.screenshot(
            path=out,
            full_page=True,
            # Fast-forwards the specimen draw to its end state instead of
            # catching it mid-stroke, which would differ on every run.
            animations="disabled",
            mask=[page.locator(sel) for sel in MASK_SELECTORS],
        )
        page.close()
        print(f"📸 wrote {out}")

    def rebuild(visible_count=None):
        env = dict(os.environ)
        if visible_count is None:
            env.pop("EXTRAS_VISIBLE_COUNT", None)
        else:
            env["EXTRAS_VISIBLE_COUNT"] = str(visible_count)
        subprocess.run([sys.executable, "src/generate.py"], check=True, env=env)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name, opts in CAPTURES:
                capture(browser, name, opts)

            name, opts = EXPANDER_CAPTURE
            rebuild(visible_count=1)
            try:
                capture(browser, name, opts, open_expander=True)
            finally:
                # Always leave dist/ holding the real page, not the fixture.
                rebuild()

            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    main()
