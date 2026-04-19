# Copilot Instructions for miketheman.dev

## Repository Overview

This is a modern, responsive personal website generator that creates a beautiful "link in bio" style page. The project uses Python with Jinja2 templating to generate a static website from TOML configuration, with automated deployment to GitHub Pages.

## Technology Stack

- **Python**: 3.13+ (minimum version required)
- **Package Manager**: [uv](https://docs.astral.sh/uv/) - Fast Python package manager; deps declared in `pyproject.toml`, pinned in `uv.lock`
- **Templating**: Jinja2 for HTML generation
- **Task Runner**: [just](https://github.com/casey/just) (optional but recommended)
- **Deployment**: GitHub Actions to GitHub Pages
- **Key Libraries**:
  - `jinja2` - Template rendering
  - `qrcode[pil]` - QR code generation with PIL support

## Project Structure

```
├── .github/
│   └── workflows/
│       ├── deploy.yml          # GitHub Actions deployment workflow
│       └── pr-preview.yml      # PR preview deployment workflow
├── src/
│   ├── generate.py             # Main site generator script
│   ├── avatar.py               # QR + portrait generator script
│   ├── icons.py                # Font Awesome SVG fetcher (reads metadata.toml)
│   ├── fonts.py                # Google Fonts self-hosting (woff2 + rewritten CSS)
│   ├── serve.py                # Development server script
│   └── snapshot.py             # Playwright visual-diff capture (dev dep)
├── assets/
│   ├── me.jpg                  # Source photo for avatar generation
│   ├── avatar.png              # QR with embedded portrait (mobile view, committed)
│   ├── avatar-plain.png        # Plain circular portrait (desktop view, committed)
│   ├── icons/                  # Font Awesome SVGs (brands/, solid/) — inlined at build time
│   ├── fonts/                  # Self-hosted Google Fonts woff2 files
│   ├── fonts.css               # Rewritten @font-face CSS — inlined into <style>
│   └── snapshots/              # PR visual-diff baselines — desktop + mobile PNGs
├── templates/
│   └── index.html.j2           # Jinja2 template for the main page
├── dist/                       # Generated website output (not committed)
├── metadata.toml               # Site configuration and content
├── metadata.example.toml       # Example configuration
├── pyproject.toml              # Project metadata and dependencies (PEP 621)
├── uv.lock                     # Pinned dependency lockfile (managed by uv)
├── .python-version             # Pinned Python (3.13)
└── justfile                    # Task runner commands
```

## Development Workflow

### Building and Testing

Dependencies live in `pyproject.toml` and are pinned in `uv.lock`. First-time setup (and after any lockfile change):

```bash
uv sync --frozen    # Install pinned deps into .venv
```

Prefer the `just` recipes — they encode the canonical invocations:

```bash
just build          # Generate the website
just serve          # Build and start development server
just avatar         # Regenerate avatar.png (QR) + avatar-plain.png (portrait)
just icons          # Fetch Font Awesome SVGs referenced in metadata.toml
just fonts          # Download + self-host Google Fonts into assets/fonts/
just lint           # Build, then biome check dist/ (HTML/CSS/a11y lint)
just snapshot       # Build, then capture desktop + mobile visual-diff PNGs
just clean          # Clean generated files
```

Fallback (if `just` isn't available, or for ad-hoc invocation) — always run from the repo root:

```bash
uv run src/generate.py
uv run src/serve.py
uv run src/avatar.py
uv run src/icons.py
uv run src/fonts.py
uv run src/snapshot.py   # requires Playwright chromium: uv run playwright install chromium
```

### Build Process

1. `src/generate.py` reads `metadata.toml`
2. Renders the Jinja2 template (`templates/index.html.j2`)
3. Outputs to `dist/index.html`
4. Copies `assets/avatar.png` and `assets/avatar-plain.png` → `dist/` if present

## Code Conventions

### Python Style

- **Python Version**: Always use features compatible with Python 3.13+
- **Script Shebang**: `#!/usr/bin/env python3`. Scripts are invoked via `just <recipe>` (preferred) or `uv run src/<script>.py` (from repo root) so they execute inside the project's `.venv`.
- **Working Directory**: Scripts use cwd-relative paths (`metadata.toml`, `templates/`, `assets/`, `dist/`). Always invoke from the repo root.
- **Error Handling**: Use try-except blocks with user-friendly error messages (with emoji prefixes)
- **Console Output**: Use emoji prefixes for status messages:
  - ✅ for success
  - ❌ for errors
  - ⚠️ for warnings
  - 🚀 for server/deployment actions
  - 🔨 for build actions
  - 🎨 for avatar/design actions

### File Organization

- Keep scripts in the root directory
- Templates in `templates/`
- Generated output in `dist/`
- Configuration in `metadata.toml`

### Configuration

- **Primary Config**: `metadata.toml` contains all site content and links
- **Format**: TOML with clear sections for profile info and links array
- **Links Order**: The order of `[[links]]` sections determines display order

## Making Changes

### Modifying Site Content

Edit `metadata.toml` to update:
- Profile information (name, title, description, avatar URL)
- Social links (URL, label, icon class)

### Modifying Layout/Style

Edit `templates/index.html.j2`:
- HTML structure
- Inline CSS styles
- Template logic

### Modifying Build Logic

Edit `generate.py`:
- Template context data
- File generation logic
- Error handling

### Creating New Features

1. Update the relevant Python script(s)
2. Ensure inline script metadata includes all required dependencies
3. Test locally with `./script.py` or `uv run script.py`
4. Update documentation if needed
5. Ensure GitHub Actions workflow continues to work

## Dependencies

### Adding New Dependencies

1. Add the package to `[project.dependencies]` in `pyproject.toml`.
2. Run `uv lock` to refresh `uv.lock`.
3. Commit both `pyproject.toml` and `uv.lock`.

CI runs `uv sync --frozen` against `uv.lock` for reproducible builds. Dependabot's `uv` ecosystem keeps the lockfile current on a weekly cadence.

### Current Dependencies

- **generate.py**: `jinja2`
- **avatar.py**: `qrcode[pil]` (includes PIL/Pillow)
- **serve.py**: No external dependencies (uses stdlib only)
- **snapshot.py**: `playwright` (dev-group only — not a runtime dep)

## Deployment

### Automatic Deployment

- **Trigger**: Push to `main` branch
- **Process**: GitHub Actions workflow (`.github/workflows/deploy.yml`)
- **Steps**:
  1. Checkout code
  2. Install uv (cached on `uv.lock`)
  3. `uv sync --frozen` to install pinned deps
  4. Build site with `uv run --frozen src/generate.py`
  5. Deploy `dist/` to GitHub Pages

### Manual Deployment

Can be triggered via GitHub Actions `workflow_dispatch` event.

## Testing

Currently, this project doesn't have automated tests. When making changes:

1. Build the site locally: `just build`
2. Test with development server: `just serve`
3. Verify the generated HTML in `dist/index.html`
4. Check that the site displays correctly in a browser
5. Verify all links work as expected

## Common Tasks

### Updating Profile Information

Edit `metadata.toml` and rebuild:
```bash
just build
just serve  # Test locally
```

### Adding a New Social Link

Add a new `[[links]]` section in `metadata.toml`:
```toml
[[links]]
url = "https://example.com/profile"
label = "Service Name"
icon = "fa-brands fa-service"  # Font Awesome icon class
```

### Changing Site Design

1. Edit `templates/index.html.j2`
2. Rebuild and test: `just serve` (builds first, then serves)
3. Check responsive design on different screen sizes
4. Verify dark mode support

### Regenerating Avatar

1. Replace `assets/me.jpg` with your own profile photo (same filename, or update `AVATAR_FILE_PATH` in `src/avatar.py`)
2. Run: `just avatar` — produces `assets/avatar.png` (QR) and `assets/avatar-plain.png` (portrait)
3. Rebuild site: `just build` — copies both into `dist/`

Note: The avatar.py script requires a personal photo file at the path you specify.

### Refreshing Visual Snapshots

After any template/CSS change, rebuild the `assets/snapshots/*.png` baselines so PR diffs reflect the intended view:

1. `just snapshot` — renders desktop (800x1400) and mobile (390x844) full-page PNGs with the volatile `.footer` masked
2. Commit the updated PNGs; GitHub's native rich image diff will show before/after on the PR

CI also regenerates these automatically on PR open/sync and commits them back if they differ.

## Important Notes

- **Generated Files**: The `dist/` directory contains generated files and should not be edited directly
- **Avatar Source**: `src/avatar.py` reads from `assets/me.jpg` (tracked in the repo). Replace that file to change the embedded photo, or edit `AVATAR_FILE_PATH` in the script.
- **Python Version**: Pinned to Python 3.13 via `.python-version` (Playwright's sync API segfaults on 3.14 due to a greenlet/freethreading interaction).
- **uv Requirement**: Scripts run inside the project's `uv`-managed `.venv`. Invoke via `just <recipe>` (preferred) or `uv run src/<script>.py` from the repo root.
- **Executable Scripts**: The `.py` scripts in `src/` are executable with proper shebangs
- **Lock File**: `uv.lock` pins the full dependency tree; it's managed by `uv lock` / `uv sync` and used by CI for reproducible builds
