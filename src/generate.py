#!/usr/bin/env python3
import datetime
import json
import os
import pathlib
import shutil
import tomllib

HUMAN_JSON_VERSION = "0.1.1"

from minijinja import Environment, load_from_path

from icons import ICON_CACHE, parse_icon

# Remaining extras hide behind "Show more" in the template. Overridable so
# `just snapshot` can build a fixture that actually renders the expander —
# with only a couple of extras it never appears on the real page.
EXTRAS_VISIBLE_COUNT = int(os.environ.get("EXTRAS_VISIBLE_COUNT", "5"))


def icon_svg(icon_class):
    """Read a cached Font Awesome SVG for inlining in the template.

    Icons are paired with a visible label, so they're marked aria-hidden
    for screen readers (the adjacent <span> carries the accessible name).
    """
    style, name = parse_icon(icon_class)
    path = ICON_CACHE / style / f"{name}.svg"
    if not path.exists():
        raise FileNotFoundError(
            f"Icon SVG missing: {path}. Run `just icons` to download."
        )
    return path.read_text().replace("<svg ", '<svg aria-hidden="true" ', 1)


def read_metadata():
    """Read and parse the TOML metadata file"""
    with open("metadata.toml", "rb") as f:
        return tomllib.load(f)


def read_fonts_css():
    path = "assets/fonts.css"
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{path} missing. Run `just fonts` to download fonts."
        )
    with open(path) as f:
        return f.read()


def file_meta(url):
    """Type and size for an extra served out of assets/files/.

    A 6 MB deck opened on venue wifi should say so before it's tapped.
    """
    if not url.startswith("files/"):
        return None
    path = pathlib.Path("assets") / url
    if not path.exists():
        return None
    size_mb = path.stat().st_size / 1_000_000
    return f"{path.suffix.lstrip('.').upper()}, {size_mb:.1f} MB"


def build_verification(metadata):
    """The identity proofs, gathered for display.

    These already exist as <head> metadata and a human.json file; this makes
    the same claims legible to a person, which is the whole point of them.

    human.json vouches are deliberately not surfaced here — that part of the
    spec is still moving. They keep shipping in dist/human.json regardless.
    """
    profile_url = next(
        (link["url"] for link in metadata.get("links", []) if link.get("rel") == "me"),
        None,
    )
    if profile_url is None:
        raise ValueError(
            'No link in metadata.toml carries rel = "me". The provenance line '
            "needs one to point at, and Mastodon needs it to verify the domain."
        )
    return {"profile_url": profile_url}


def generate_html(metadata):
    env = Environment(loader=load_from_path("templates"))
    env.add_function("icon_svg", icon_svg)

    visible_extras = []
    expandable_extras = []

    if "extras" in metadata and metadata["extras"]:
        parsed_extras = []
        for i, extra in enumerate(metadata["extras"]):
            if "date" not in extra:
                raise ValueError(
                    f"Extras item {i+1} ('{extra.get('label', 'unknown')}') is missing required 'date' field"
                )
            try:
                parsed_date = datetime.datetime.strptime(extra["date"], "%Y-%m-%d")
                parsed_extras.append((parsed_date, extra))
            except ValueError:
                raise ValueError(
                    f"Extras item {i+1} ('{extra.get('label', 'unknown')}') has invalid date format. "
                    f"Expected ISO 8601 format (YYYY-MM-DD), got: {extra['date']}"
                )

        parsed_extras.sort(key=lambda x: x[0], reverse=True)
        metadata["extras"] = [extra for _, extra in parsed_extras]

        for extra in metadata["extras"]:
            meta = file_meta(extra["url"])
            if meta:
                extra["filemeta"] = meta

        visible_extras = metadata["extras"][:EXTRAS_VISIBLE_COUNT]
        expandable_extras = metadata["extras"][EXTRAS_VISIBLE_COUNT:]

    metadata["visible_extras"] = visible_extras
    metadata["expandable_extras"] = expandable_extras

    context = {
        **metadata,
        # ISO, like every other date on the page — the extras dates and the
        # vouch stamp. One date language per sheet.
        "updated_date": datetime.date.today().isoformat(),
        "verification": build_verification(metadata),
        "fonts_css": read_fonts_css(),
    }

    html = env.render_template("index.html.j2", **context)
    with open("dist/index.html", "w") as f:
        f.write(html)


def generate_human_json(metadata):
    payload = {"version": HUMAN_JSON_VERSION, **metadata["human"]}
    with open("dist/human.json", "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def main():
    try:
        os.makedirs("dist", exist_ok=True)

        metadata = read_metadata()
        generate_html(metadata)
        generate_human_json(metadata)

        missing = []
        for name in (
            "avatar.png",
            "avatar.webp",
            "avatar-plain.png",
            "avatar-plain.webp",
            "favicon.png",
            "og.png",
        ):
            try:
                shutil.copy(f"assets/{name}", f"dist/{name}")
            except FileNotFoundError:
                missing.append(name)

        if os.path.isdir("assets/fonts"):
            shutil.copytree("assets/fonts", "dist/fonts", dirs_exist_ok=True)
        else:
            missing.append("fonts/")

        # Downloadable files (PDFs, etc.) referenced by [[extras]] via url = "files/...".
        if os.path.isdir("assets/files"):
            shutil.copytree("assets/files", "dist/files", dirs_exist_ok=True)

        if missing:
            print(f"⚠️  Website generated, but missing: {', '.join(missing)}. Run `just avatar` / `just fonts` / `just og` to regenerate.")
        else:
            print("✅ Website generated successfully in dist/")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure metadata.toml exists and is properly formatted.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
