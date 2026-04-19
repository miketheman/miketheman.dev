#!/usr/bin/env python3
"""Download Google Fonts CSS + woff2 files for self-hosting.

Writes woff2 files to assets/fonts/ and a rewritten CSS to assets/fonts.css
with local relative URLs. The CSS is inlined into the rendered page by
generate.py, eliminating the render-blocking external CSS request.
"""
import pathlib
import re
import urllib.request

FONTS_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Fraunces:opsz,wght@9..144,400"
    "&family=Hanken+Grotesk:wght@400;500"
    "&display=swap"
)
FONTS_DIR = pathlib.Path("assets/fonts")
CSS_OUT = pathlib.Path("assets/fonts.css")

# Modern Firefox UA so Google returns woff2 + (where available) variable-font files.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) "
    "Gecko/20100101 Firefox/123.0"
)
FONT_URL_RE = re.compile(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as r:
        return r.read()


def main():
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    css = fetch(FONTS_URL).decode("utf-8")

    urls = sorted(set(FONT_URL_RE.findall(css)))
    for url in urls:
        name = url.rsplit("/", 1)[-1]
        dest = FONTS_DIR / name
        if not dest.exists():
            print(f"📦 {name}")
            dest.write_bytes(fetch(url))

    # Rewrite gstatic URLs to local relative paths for self-hosting.
    local_css = FONT_URL_RE.sub(
        lambda m: f"url(fonts/{m.group(1).rsplit('/', 1)[-1]})", css
    )
    CSS_OUT.write_text(local_css)
    print(f"✅ wrote {CSS_OUT} ({len(urls)} font file(s))")


if __name__ == "__main__":
    main()
