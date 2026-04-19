# miketheman.dev

A modern, responsive personal website generator that creates a beautiful "link in bio" style page. Features a QR code avatar and clean design that adapts to light/dark themes.

## ✨ Features

- **QR Code Avatar**: Automatically generates a QR code with embedded profile photo
- **Responsive Design**: Looks great on desktop and mobile devices
- **Dark Mode Support**: Automatically adapts to user's system preference
- **Easy Configuration**: Simple TOML file for all content and links
- **Extras Section**: Optional section for presentations, talks, and additional resources
- **Fast Generation**: Uses Python with Jinja2 templating
- **GitHub Actions Deploy**: Automated deployment to GitHub Pages

## 🚀 Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- [just](https://github.com/casey/just) - Command runner (optional but recommended)

### Build the Site

First-time setup (or after `uv.lock` changes):

```bash
uv sync --frozen    # Install pinned dependencies into .venv
```

Then:

```bash
# Using Just (recommended)
just build          # Generate the website
just serve          # Build and start development server
just avatar         # Regenerate avatar.png (QR) and avatar-plain.png (portrait)
just icons          # Fetch Font Awesome SVGs referenced in metadata.toml
just fonts          # Download + self-host Google Fonts into assets/fonts/
just lint           # Build, then run biome against dist/index.html (HTML/CSS/a11y lint)
just snapshot       # Build, then capture desktop + mobile PNG snapshots for PR visual diffs
just clean          # Clean generated files

# Or run scripts directly (from repo root)
uv run src/generate.py  # Generate the website
uv run src/serve.py     # Start development server
uv run src/avatar.py    # Generate avatars from assets/me.jpg
uv run src/icons.py     # Download Font Awesome SVGs for metadata.toml icons
uv run src/fonts.py     # Download Google Fonts woff2 + rewrite CSS to self-host
uv run src/snapshot.py  # Capture visual-diff snapshots (requires Playwright chromium)
```

The resulting website will be created in the `dist/` directory.

### Configuration

Edit `metadata.toml` to customize your profile:

```toml
name = "Your Name"
title = "Your Title"
avatar = "https://yoursite.com/avatar.png"

[[links]]
url = "https://github.com/yourusername"
label = "GitHub"
icon = "fa-brands fa-github"

# Optional: Add extras section for presentations, talks, resources, etc.
[[extras]]
label = "PyCon 2024 - My Talk"
url = "https://example.com/slides"
icon = "fa-solid fa-presentation"
date = "2024-05-15"  # Required: ISO 8601 date format (YYYY-MM-DD)
```

#### Extras Section

The optional `extras` section allows you to showcase additional content like:

- Conference presentations and talks
- Slide decks and resources
- Video recordings
- Appendix materials

Extras are automatically sorted by date (most recent first). If more than 5 items are present, the additional items will be hidden behind an expandable "Show more" button.

Each extra item supports:

- `label`: Display text for the item
- `url`: Link to the resource
- `icon`: FontAwesome icon class
- `date`: **Required** - Date in ISO 8601 format (YYYY-MM-DD) for sorting

## 📁 Project Structure

```text
├── pyproject.toml        # Project metadata and dependencies (runtime + dev)
├── uv.lock               # Pinned dependency lockfile
├── .python-version       # Pinned Python (3.13)
├── justfile              # Task runner commands
├── metadata.toml         # Site configuration
├── src/                  # Scripts (run from repo root via uv run)
│   ├── generate.py       # Main site generator
│   ├── avatar.py         # QR + portrait generator
│   ├── icons.py          # Font Awesome SVG fetcher (reads metadata.toml)
│   ├── fonts.py          # Google Fonts self-hosting (woff2 + rewritten CSS)
│   ├── serve.py          # Development server
│   └── snapshot.py       # Playwright visual-diff capture (dev dep)
├── assets/               # Source + generated images (committed)
│   ├── me.jpg            # Source photo for avatar
│   ├── avatar.png        # QR with embedded portrait (mobile view)
│   ├── avatar-plain.png  # Plain circular portrait (desktop view)
│   ├── icons/            # Font Awesome SVGs (brands/ + solid/) — inlined at build time
│   ├── fonts/            # Self-hosted woff2 files — copied to dist/fonts/ at build
│   ├── fonts.css         # Rewritten @font-face CSS — inlined into <style> at build
│   └── snapshots/        # PR visual-diff baselines (desktop + mobile PNGs)
├── templates/            # Jinja2 templates
│   └── index.html.j2     # Main page template
└── dist/                 # Generated website (gitignored)
    ├── index.html
    ├── avatar.png
    └── avatar-plain.png
```

## 🚀 Deploy

Deployment is handled automatically via GitHub Actions when you push to the main branch. The workflow builds the site and deploys it to GitHub Pages.

### Pull Request Previews

When you create a pull request, a preview of your changes is automatically deployed to a unique URL and linked in the PR description. This allows you to review changes before merging. The preview is automatically cleaned up when the PR is closed.

### Visual Diffs

The preview workflow also regenerates `assets/snapshots/*.png` via Playwright (desktop + mobile viewports). If the rendered snapshot differs from the committed baseline, the workflow commits the updated PNG back to the PR branch — GitHub's native rich image diff then shows a swipe/2-up comparison on the PR's Files tab.

## 🎨 Customization

- **Styling**: Modify the CSS in `templates/index.html.j2`
- **Layout**: Update the Jinja2 template structure
- **Links**: Add/remove social links in `metadata.toml`
- **Extras**: Add optional extras section for presentations and resources
- **Avatar**: Replace `assets/me.jpg` with your own photo and run `just avatar`
