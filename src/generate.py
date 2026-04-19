#!/usr/bin/env python3
import datetime
import os
import shutil
import tomllib

from jinja2 import Environment, FileSystemLoader

EXTRAS_VISIBLE_COUNT = 5  # remaining extras hide behind "Show more" in the template


def read_metadata():
    """Read and parse the TOML metadata file"""
    with open("metadata.toml", "rb") as f:
        return tomllib.load(f)


def generate_html(metadata):
    env = Environment(loader=FileSystemLoader("templates"))
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
    }

    html = template.render(**context)
    with open("dist/index.html", "w") as f:
        f.write(html)


def main():
    try:
        os.makedirs("dist", exist_ok=True)

        metadata = read_metadata()
        generate_html(metadata)

        if os.path.exists("assets/avatar.png"):
            shutil.copy("assets/avatar.png", "dist/avatar.png")
            print("✅ Website generated successfully in dist/")
        else:
            print("⚠️  Website generated, but assets/avatar.png not found. Run `just avatar` to generate it.")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure metadata.toml exists and is properly formatted.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
