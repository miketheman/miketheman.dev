# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This is a `uv`-managed application project: `pyproject.toml` declares deps, `uv.lock` pins them. `uv sync --frozen` creates/refreshes `.venv`; `uv run <script>` executes inside it. **All scripts expect to be run from the repo root** (paths are cwd-relative).

```bash
just build     # uv run src/generate.py — render metadata.toml + templates/index.html.j2 into dist/index.html
just serve     # build, then uv run src/serve.py (stdlib http.server on :8000, opens browser)
just avatar    # uv run src/avatar.py — regenerates assets/avatar.png
just clean     # rm dist/index.html dist/avatar.png
```

First run (or after `uv.lock` changes): `uv sync --frozen` to install deps into `.venv`.

## Layout

```
pyproject.toml / uv.lock    # deps
metadata.toml               # site content
templates/index.html.j2     # single-page template with inline CSS
src/                        # scripts (cwd-relative — run from repo root)
assets/                     # me.jpg (source photo) + avatar.png (generated QR, committed)
dist/                       # build output (gitignored)
```

## Architecture

Three scripts sharing one project env:

- **src/generate.py** (uses `jinja2`): reads `metadata.toml`, validates and sorts `[[extras]]` by ISO date descending, splits into `visible_extras` (first 5) and `expandable_extras` (rest), renders `templates/index.html.j2` → `dist/index.html`, copies `assets/avatar.png` → `dist/avatar.png`.
- **src/avatar.py** (uses `qrcode[pil]`): builds a QR code encoding `https://miketheman.dev` with a circular-cropped photo embedded in the center. Reads `assets/me.jpg`, writes `assets/avatar.png`.
- **src/serve.py** (stdlib only): dev server rooted at `dist/`. Errors cleanly if `generate.py` hasn't run.

Template is a single Jinja2 file with inline `<style>` (no separate CSS pipeline). Dark mode via `prefers-color-scheme`. Visual changes mean editing `templates/index.html.j2` directly.

Both `assets/me.jpg` and `assets/avatar.png` are committed. `avatar.png` is derived but committed because CI doesn't regenerate it — rerun `just avatar` locally after changing the source photo.

## Extras validation

`src/generate.py` raises `ValueError` if any `[[extras]]` entry is missing `date` or has a non-`YYYY-MM-DD` date. New entry types must carry a parseable date.

## Adding Python dependencies

Add to `[project.dependencies]` in `pyproject.toml`, then `uv lock` to refresh `uv.lock`. CI uses `uv sync --frozen` against `uv.lock` for reproducible builds. Dependabot's `uv` ecosystem keeps `uv.lock` current on a weekly cadence.

## Deployment

- `.github/workflows/deploy.yml` — push to `main` runs `uv sync --frozen` + `src/generate.py` and publishes `dist/` to GitHub Pages. Also supports `workflow_dispatch`.
- `.github/workflows/pr-preview.yml` — PRs get an isolated preview URL; cleaned up on close.

Both workflows cache on `uv.lock` via `astral-sh/setup-uv`.

## Testing

No automated tests. Verify changes by running `just serve` and checking the rendered page (layout, links, dark mode, extras expand/collapse if >5 items).
