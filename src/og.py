#!/usr/bin/env python3
"""Render templates/og.html.j2 to assets/og.png via Playwright.

Produces the 1200×630 OpenGraph card used in <head> meta tags. The rendered
HTML is written to assets/.og.html (gitignored) so relative URLs to fonts.css
and avatar-plain.png resolve without a <base href>. The dotfile is removed
after screenshotting.
"""
import tomllib
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import ViewportSize, sync_playwright

ASSETS = Path("assets")
OG_PNG = ASSETS / "og.png"
TMP_HTML = ASSETS / ".og.html"
VIEWPORT: ViewportSize = {"width": 1200, "height": 630}


def read_metadata():
    with open("metadata.toml", "rb") as f:
        return tomllib.load(f)


def guard_inputs():
    if not (ASSETS / "avatar-plain.png").exists():
        raise SystemExit("❌ assets/avatar-plain.png missing. Run `just avatar` first.")
    if not (ASSETS / "fonts.css").exists() or not any((ASSETS / "fonts").glob("*.woff2")):
        raise SystemExit("❌ assets/fonts.css or assets/fonts/*.woff2 missing. Run `just fonts` first.")


def render_template(metadata):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("og.html.j2")
    return template.render(
        name=metadata["name"],
        seo_title=metadata["seo_title"],
        site_url=metadata["site_url"],
    )


def main():
    guard_inputs()
    metadata = read_metadata()
    html = render_template(metadata)
    TMP_HTML.write_text(html)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport=VIEWPORT, device_scale_factor=1)
            page.goto(f"file://{TMP_HTML.resolve()}", wait_until="networkidle")
            # Ensure woff2 is actually rendered before the shot.
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(OG_PNG), type="png", full_page=False)
            browser.close()
    finally:
        TMP_HTML.unlink(missing_ok=True)

    print(f"📸 wrote {OG_PNG} ({VIEWPORT['width']}×{VIEWPORT['height']})")


if __name__ == "__main__":
    main()
