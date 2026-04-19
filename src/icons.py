#!/usr/bin/env python3
"""Download Font Awesome SVGs referenced in metadata.toml.

Writes to assets/icons/{style}/{name}.svg. The cache is committed to the
repo so builds are reproducible and don't touch the network.
"""
import pathlib
import re
import tomllib
import urllib.request

FA_VERSION = "7.2.0"
FA_URL_TMPL = (
    "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@"
    f"{FA_VERSION}/svgs/{{style}}/{{name}}.svg"
)
ICON_CACHE = pathlib.Path("assets/icons")
ICON_RE = re.compile(r"fa-(brands|solid|regular)\s+fa-([a-z0-9-]+)")


def parse_icon(icon_class):
    m = ICON_RE.search(icon_class)
    if not m:
        raise ValueError(f"Unrecognized icon class: {icon_class!r}")
    return m.group(1), m.group(2)


def collect_icons():
    with open("metadata.toml", "rb") as f:
        metadata = tomllib.load(f)
    classes = {item["icon"] for item in metadata.get("links", [])}
    classes |= {item["icon"] for item in metadata.get("extras", [])}
    return {parse_icon(c) for c in classes}


def fetch(style, name):
    dest = ICON_CACHE / style / f"{name}.svg"
    if dest.exists():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = FA_URL_TMPL.format(style=style, name=name)
    print(f"📦 {style}/{name} ← {url}")
    try:
        with urllib.request.urlopen(url) as response:
            dest.write_bytes(response.read())
    except Exception as e:
        raise SystemExit(f"❌ failed to fetch {url}: {e}")
    return True


def main():
    fetched = sum(fetch(*icon) for icon in sorted(collect_icons()))
    if fetched:
        print(f"✅ fetched {fetched} new icon(s)")
    else:
        print("✅ icons up to date")


if __name__ == "__main__":
    main()
