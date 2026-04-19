#!/usr/bin/env python3
import datetime
import json
import os
import shutil
import tomllib

HUMAN_JSON_VERSION = "0.1.1"

from jinja2 import Environment, FileSystemLoader

from icons import ICON_CACHE, parse_icon

EXTRAS_VISIBLE_COUNT = 5  # remaining extras hide behind "Show more" in the template


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


def generate_html(metadata):
    env = Environment(loader=FileSystemLoader("templates"))
    env.globals["icon_svg"] = icon_svg
    template = env.get_template("index.html.j2")

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

        visible_extras = metadata["extras"][:EXTRAS_VISIBLE_COUNT]
        expandable_extras = metadata["extras"][EXTRAS_VISIBLE_COUNT:]

    metadata["visible_extras"] = visible_extras
    metadata["expandable_extras"] = expandable_extras

    context = {
        **metadata,
        "updated_date": datetime.datetime.now().strftime("%B %d, %Y"),
        "fonts_css": read_fonts_css(),
    }

    html = template.render(**context)
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
        for name in ("avatar.png", "avatar-plain.png"):
            try:
                shutil.copy(f"assets/{name}", f"dist/{name}")
            except FileNotFoundError:
                missing.append(name)

        if os.path.isdir("assets/fonts"):
            shutil.copytree("assets/fonts", "dist/fonts", dirs_exist_ok=True)
        else:
            missing.append("fonts/")

        if missing:
            print(f"⚠️  Website generated, but missing: {', '.join(missing)}. Run `just avatar` / `just fonts` to regenerate.")
        else:
            print("✅ Website generated successfully in dist/")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure metadata.toml exists and is properly formatted.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
