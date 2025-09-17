#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "jinja2",
# ]
# ///
import datetime
import shutil
import tomllib

from jinja2 import Environment, FileSystemLoader


def read_metadata():
    """Read and parse the TOML metadata file"""
    with open("metadata.toml", "rb") as f:
        return tomllib.load(f)


def generate_html(metadata):
    """Generate HTML from metadata using Jinja2 template"""
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html.j2")

    # Add additional context for the template
    context = {
        **metadata,
        "updated_date": datetime.datetime.now().strftime("%B %d, %Y"),
    }

    # Render template with context
    html = template.render(**context)

    # Write the generated HTML to a file
    with open("dist/index.html", "w") as f:
        f.write(html)


def main():
    try:
        # Ensure dist directory exists
        import os
        os.makedirs("dist", exist_ok=True)

        metadata = read_metadata()
        generate_html(metadata)

        # Copy avatar.png to dist if it exists
        if os.path.exists("avatar.png"):
            shutil.copy("avatar.png", "dist/avatar.png")
            print("✅ Website generated successfully in dist/")
        else:
            print("⚠️  Website generated, but avatar.png not found. Run ./avatar.py to generate it.")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure metadata.toml exists and is properly formatted.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
