# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Four confirmed audiences, all arriving cold and leaving quickly:

1. **In-person encounters** — someone who just watched a talk, met Mike at a conference, or scanned the QR-code avatar off a slide or badge. Phone, hallway, seconds of attention, deciding whether to follow.
2. **Python / PyPI community** — packaging users, contributors, and fellow maintainers who arrived from PyPI, a blog post, or a GitHub thread and want to know who this is and where he writes.
3. **Press, conference organizers, and recruiters** — vetting credentials, looking for a bio, a usable photo, and a reachable channel.
4. **Mike himself** — the page is the self-owned canonical link hub he points people at, independent of any platform he doesn't control.

## Product Purpose

A single-page personal identity hub for Mike Fiedler ("Code Gardener"; PyPI maintainer, open source contributor, Python packaging and developer experience). It answers "who is this person and where do I find them" in one screen and routes visitors to the places he actually publishes.

Success is any of three outcomes, weighted equally:

- the visitor follows him somewhere (GitHub, Bluesky, Mastodon, LinkedIn, personal blog, PyPI blog);
- the visitor can verify this is genuinely him and that the accounts are his;
- the visitor leaves with a sense of the person, not just a list of URLs.

Deck downloads and talk companions are real content and matter, but they are not the primary success metric.

## Positioning

Not a résumé, not a blog, not a hosted link-in-bio service. It is a self-owned, self-contained identity page whose distinguishing mechanism is *verifiable identity*: the QR-code avatar with an embedded portrait is the same artifact used on slides and in person, `rel="me"` links prove the Mastodon account, and `human.json` (with vouches from other real people) makes the identity claim machine-readable. The page's job is to make "yes, this is the same Mike Fiedler" cheap to confirm.

## Operating Context

- The URL is most often reached by scanning a QR code or typing a short domain seen on a conference slide — mobile-first, low-patience, sometimes on venue wifi.
- The QR avatar is dual-purpose: it lives on the page *and* circulates on slides, stickers, and badges as Mike's identity device.
- Content lives in `metadata.toml`: profile fields, an ordered `[[links]]` list, dated `[[extras]]` (talks, companion gists, PDF decks served from `assets/files/`), and a `[human]` block emitted as `dist/human.json`.
- Extras are sorted newest-first; the first five show and the rest are behind an expander, so the list grows over time without growing the page.
- Publishing is push-to-`main` → GitHub Actions → GitHub Pages. PRs get a preview URL and regenerated visual snapshots.

## Capabilities and Constraints

- **Current build:** one static HTML page, no runtime JavaScript, self-hosted fonts and inlined Font Awesome SVGs, no analytics, nothing third-party fetched at page load.
- **That is a preference, not a rule.** Mike's stated stance: keep things lightweight, but he can imagine adding infrastructure that earns its place — e.g. Plausible analytics, or hypermedia components from [fixi](https://fixiproject.org/) / htmx. Design work may propose such additions with justification; it should not assume a hard no-JS ceiling, and it should not add weight casually.
- **Planned:** embedding/federating blog posts from another site he owns (miketheman.net). Design should anticipate a recent-posts section as a first-class part of the layout, not a bolt-on.
- Content is authored in TOML by hand; every `[[extras]]` entry must carry a parseable `YYYY-MM-DD` date or the build fails.
- The avatar exists in two forms, chosen by media query: the QR code on touch/narrow devices, the plain circular portrait on desktop.

## Brand Commitments

- Name: **Mike Fiedler**. Self-described title: **Code Gardener**.
- The QR-code-with-embedded-portrait avatar is an established identity device already in circulation offline. Treat it as an asset, not a decoration to be swapped out casually.
- Voice in existing copy is plain and unpretentious ("Building better software, one commit at a time"), with no self-promotional inflation.
- Stated design stance for future work: **clean and focused, but with character.** Minimal is the baseline; personality-free is not the goal.

## Evidence on Hand

- Real assets, all committed: `assets/me.jpg` (source photo), `assets/avatar.png` (QR), `assets/avatar-plain.png` (portrait), `assets/favicon.png` (tab icon), `assets/og.png`, `assets/icons/**`, `assets/fonts/**`, `assets/snapshots/*.png`.
- Real content: six profile links, dated extras including a DevOpsDays Tel Aviv 2025 talk companion gist and a "Trusted Publishing" PDF deck (`assets/files/Trusted-Publishing.pdf`).
- Real identity proofs: `rel="me"` to hachyderm.io, `human.json` with a dated vouch from sethmlarson.dev.
- **Not on hand — do not fabricate:** testimonials, client or employer logos, metrics, download counts, awards, pricing, availability-for-hire claims, or a contact email. No email address is currently published anywhere on the page.

## Product Principles

1. **One screen, one job.** A visitor should get identity, credibility, and a way onward without hunting. Growth in content must not become growth in scroll.
2. **Verifiability is the feature.** `rel="me"`, `human.json`, the consistent portrait, and the QR device all exist so a stranger can confirm this is the real person. Preserve and strengthen these signals.
3. **The QR avatar is the anchor.** It is the bridge between the physical encounter and the page; it earns its prominence.
4. **Lightweight until proven otherwise.** Self-hosted, privacy-respecting, fast on venue wifi. New dependencies, scripts, or third-party calls are allowed but must be argued for.
5. **Character without noise.** Restraint is the register, not blandness. The personality lives in the details.

## Accessibility & Inclusion

No product-specific standard was established by the user. Factual current state: rendered output is linted by Biome for HTML/CSS/a11y issues (including SVGs missing `aria-hidden`/`<title>`), and a lint failure blocks deploy and preview.
