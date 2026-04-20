# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This is a `uv`-managed application project: `pyproject.toml` declares deps, `uv.lock` pins them. `uv sync --frozen` creates/refreshes `.venv`; `uv run <script>` executes inside it. **All scripts expect to be run from the repo root** (paths are cwd-relative).

```bash
just build     # uv run src/generate.py — render metadata.toml + templates/index.html.j2 into dist/index.html
just serve     # build, then uv run src/serve.py (stdlib http.server on :8000, opens browser)
just avatar    # uv run src/avatar.py — regenerates assets/avatar.png + assets/avatar-plain.png
just icons     # uv run src/icons.py — fetches Font Awesome SVGs referenced in metadata.toml into assets/icons/
just og        # uv run src/og.py — render templates/og.html.j2 → assets/og.png (1200x630 OG card)
just fonts     # uv run src/fonts.py — downloads Google Fonts woff2 + rewrites CSS to self-host (assets/fonts/)
just lint      # build, then biome check dist/ — HTML/CSS/a11y lint on rendered output
just snapshot  # build, then uv run src/snapshot.py — captures desktop + mobile PNG snapshots for PR visual diffs
just clean     # rm dist/index.html dist/avatar*.png
```

Biome is expected to be on `PATH` locally (`brew install biome` or similar). CI installs it via the pinned `biomejs/setup-biome` action.

First run (or after `uv.lock` changes): `uv sync --frozen` to install deps into `.venv`. Python is pinned to 3.13 via `.python-version` (greenlet/Playwright sync API crashes on 3.14).

## Layout

```
pyproject.toml / uv.lock    # deps (runtime + dev group with playwright)
.python-version             # pinned to 3.13
metadata.toml               # site content
templates/index.html.j2     # single-page template with inline CSS + design tokens
src/                        # scripts (cwd-relative — run from repo root)
assets/                     # me.jpg (source photo) + avatar.png + avatar-plain.png (all committed)
assets/icons/               # Font Awesome SVGs cached at brands/ and solid/, inlined at build time
assets/fonts/               # self-hosted Google Fonts woff2 files (copied to dist/fonts/ at build)
assets/fonts.css            # rewritten @font-face CSS inlined into the rendered page
assets/snapshots/           # homepage.png + homepage-mobile.png — PR visual-diff baselines
dist/                       # build output (gitignored)
```

## Architecture

Seven scripts sharing one project env:

- **src/generate.py** (uses `jinja2`): reads `metadata.toml`, validates and sorts `[[extras]]` by ISO date descending, splits into `visible_extras` (first 5) and `expandable_extras` (rest), renders `templates/index.html.j2` → `dist/index.html`, writes the `[human]` block as `dist/human.json` (with `version` prepended — see https://codeberg.org/robida/human.json), copies `assets/avatar.png`, `assets/avatar-plain.png`, and the `assets/fonts/` directory into `dist/`. Inlines the contents of `assets/fonts.css` into the rendered `<style>` block and registers an `icon_svg()` Jinja global that reads pre-cached Font Awesome SVGs from `assets/icons/` and inlines them (no FA CSS/webfonts at runtime).
- **src/avatar.py** (uses `qrcode[pil]`): builds a QR code encoding `https://miketheman.dev` with a circular-cropped photo embedded in the center. Reads `assets/me.jpg`, writes `assets/avatar.png` (the QR) AND `assets/avatar-plain.png` (just the circular portrait, used on desktop via `<picture>`).
- **src/icons.py** (stdlib only): parses `fa-{style} fa-{name}` classes from `metadata.toml`, downloads missing SVGs from `cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@{version}/svgs/{style}/{name}.svg` into `assets/icons/{style}/{name}.svg`. Existing files are skipped. Version is pinned in the script.
- **src/fonts.py** (stdlib only): downloads the Google Fonts CSS for Fraunces + Hanken Grotesk, fetches every referenced `fonts.gstatic.com/*.woff2`, rewrites the CSS with local `url(fonts/<name>.woff2)` references, and writes both the rewritten CSS (`assets/fonts.css`) and the woff2 files (`assets/fonts/*.woff2`). Existing woff2 files are skipped.
- **src/serve.py** (stdlib only): dev server rooted at `dist/`. Errors cleanly if `generate.py` hasn't run.
- **src/snapshot.py** (dev-group dep: `playwright`): captures two full-page PNGs — `assets/snapshots/homepage.png` (800x1400 desktop viewport) and `assets/snapshots/homepage-mobile.png` (390x844, `is_mobile=True`). Masks the `.footer` (volatile date). Baselines are committed; PRs regenerate and get GitHub's native rich image diff.
- **src/og.py** (dev-group dep: `playwright`): renders `templates/og.html.j2` to `assets/og.png`, a 1200×630 OpenGraph card used in `<head>` meta tags. Uses the site's dark-mode tokens and self-hosted fonts so the OG preview matches the site. Reads `seo_title`, `name`, and `site_url` from `metadata.toml`. Writes the rendered HTML to `assets/.og.html` (gitignored) so relative asset URLs resolve, then deletes it after screenshotting.

Template is a single Jinja2 file with inline `<style>` organized as `@layer tokens, base, components` (design tokens in `:root`, dark-mode overrides via `prefers-color-scheme`). Visual changes mean editing `templates/index.html.j2` directly.

The page shows the QR avatar on touch/narrow devices and the plain circular portrait on desktop via `<picture>` with media `(min-width: 640px) and (hover: hover) and (pointer: fine)`. The in-page `<img>` uses a relative path (`avatar.png`); `{{ avatar }}` in OG/Twitter meta keeps the absolute URL.

`assets/me.jpg`, `assets/avatar.png`, `assets/avatar-plain.png`, `assets/og.png`, `assets/icons/**`, `assets/fonts/**`, `assets/fonts.css`, and `assets/snapshots/*.png` are all committed — CI doesn't regenerate them. After changing metadata: `just icons` (if you referenced a new FA icon) before `just build`. After the source photo changes: `just avatar`. After a font-family / weight change: update `src/fonts.py` and `just fonts`. After visual changes: `just snapshot`. After changing `seo_title`, `seo_description`, `name`, `site_url`, or the OG card template/style: `just og`.

## Extras validation

`src/generate.py` raises `ValueError` if any `[[extras]]` entry is missing `date` or has a non-`YYYY-MM-DD` date. New entry types must carry a parseable date.

## Adding Python dependencies

Add to `[project.dependencies]` in `pyproject.toml`, then `uv lock` to refresh `uv.lock`. CI uses `uv sync --frozen` against `uv.lock` for reproducible builds. Dependabot's `uv` ecosystem keeps `uv.lock` current on a weekly cadence.

## Deployment

- `.github/workflows/deploy.yml` — push to `main` runs `uv sync --frozen` + `src/generate.py` and publishes `dist/` to GitHub Pages. Also supports `workflow_dispatch`.
- `.github/workflows/pr-preview.yml` — PRs get an isolated preview URL AND regenerate `assets/snapshots/*.png` via Playwright. If the rendered snapshots differ, the workflow commits them back to the PR branch (authored as the PR user to avoid a `Co-authored-by: github-actions[bot]` trailer on squash-merge). `actions/cache` warms the Chromium download across runs.

Both workflows cache uv deps on `uv.lock` via `astral-sh/setup-uv`. Workflows pass `zizmor` (SHA-pinned actions, no persisted credentials, template-injection-free).

## Testing

No automated unit tests. Two forms of verification:

1. **Lint** (`just lint`): `biome check dist/index.html` — catches HTML/CSS/a11y issues on the rendered output (e.g., SVGs without `aria-hidden`/`<title>`, duplicate CSS properties). Config lives in `biome.json`, scoped to `dist/**/*.html`. Both `deploy.yml` and `pr-preview.yml` run this step after build; a lint failure blocks deploy/preview.
2. **Visual**: `just serve` (interactive browser check) or `just snapshot` (deterministic PNGs, mobile + desktop). PR-time: the preview workflow regenerates snapshots, commits them back if changed, and GitHub's rich image diff shows swipe/2-up on the PR's Files tab.
