---
name: miketheman.dev
description: A pressed-specimen identity sheet — warm paper, one green, hairline rules, no shadows.
colors:
  paper: "#f4f1ea"
  ink: "#1c1a17"
  ink-muted: "#5a554d"
  ink-subtle: "#6b6559"
  rule: "#d8d2c4"
  surface-hover: "#ebe4d4"
  pressed-fern: "#3f5a3a"
  qr-white: "#ffffff"
  night-paper: "#14130f"
  night-ink: "#ece7d9"
  night-ink-muted: "#a6a094"
  night-ink-subtle: "#90897d"
  night-rule: "#2d2b26"
  night-surface-hover: "#1e1c17"
  new-growth: "#a2c087"
typography:
  display:
    fontFamily: "Petrona, ui-serif, Georgia, serif"
    fontSize: "clamp(2.0625rem, 1.77rem + 1.56vw, 2.875rem)"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(0.875rem, 0.85rem + 0.15vw, 0.9375rem)"
    fontWeight: 500
    letterSpacing: "0.14em"
  body:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(1rem, 0.96rem + 0.20vw, 1.0625rem)"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(0.75rem, 0.73rem + 0.10vw, 0.8125rem)"
    fontWeight: 500
    letterSpacing: "0.14em"
  meta:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(0.75rem, 0.73rem + 0.10vw, 0.8125rem)"
    fontWeight: 400
    letterSpacing: "0.06em"
    fontFeature: "'tnum'"
rounded:
  sm: "2px"
  full: "50%"
spacing:
  1: "0.25rem"
  2: "0.5rem"
  3: "0.75rem"
  4: "1rem"
  5: "1.5rem"
  7: "3rem"
components:
  link-row:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "1rem 1.5rem"
  link-row-hover:
    backgroundColor: "{colors.surface-hover}"
    textColor: "{colors.ink}"
  expander-summary:
    backgroundColor: "transparent"
    textColor: "{colors.ink-muted}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "0.75rem 1rem"
  expander-summary-hover:
    backgroundColor: "{colors.surface-hover}"
  avatar-mat:
    backgroundColor: "{colors.qr-white}"
    padding: "1.5rem"
    width: "512px"
  avatar-portrait:
    backgroundColor: "transparent"
    rounded: "{rounded.full}"
  section-heading:
    textColor: "{colors.ink-muted}"
    typography: "{typography.label}"
  date-stamp:
    textColor: "{colors.ink-subtle}"
    typography: "{typography.meta}"
---

# Design System: miketheman.dev

## Overview

**Creative North Star: "The Herbarium Sheet"**

The page is a specimen mounted on warm paper. The QR avatar sits inside a double-ruled mat — an outer border and an inner hairline inset 8px from it — the way a pressed leaf is framed and labeled on an archival sheet. Below it the name is set once in a warm humanist serif, the role is a tracked-out caps line held between two short green rules, and every link is a hairline-bordered entry mounted in the same column. Where a lesser page would put a `<hr>`, this one draws a leaf.

The register is handmade and tactile, with a little wryness. The hand is visible on purpose: the ornament is a four-command SVG path someone plotted by hand, not a glyph from an icon set; the display face is a warm humanist serif whose letterforms keep a drawn, faintly calligraphic hand rather than a drafted one; the accent green is the color of a dried specimen rather than a brand. Nothing here is generated-looking, and nothing here shouts. There is exactly one chromatic voice on the entire page, and it is used about six times.

Density is generous and vertical. One column, 36rem wide, centered in the viewport, stacked at a 1.5rem rhythm — the page is meant to be read in a hallway on a phone, seconds after someone scanned the code that is now looking back at them from the screen. It explicitly rejects the bio-link SaaS look (pill buttons, gradient hero, candy cards), the dev-portfolio dark-neon look (terminal green on black, mono everything, glow), and the generic SaaS landing look (rounded-xl cards, blue-500, soft drop shadows, Inter).

**Key Characteristics:**

- Warm paper and ink, never white-and-gray
- One green, used sparingly, as the only chroma
- Hairline rules do all structural work; zero shadows
- Near-square 2px corners — the desktop portrait is the only circle
- Serif display voice used exactly once; everything else humanist grotesque
- Uppercase, widely tracked labels for anything secondary
- A drawn botanical ornament in place of a divider

## Colors

Warm paper stock and warm-black ink, with a single dried-botanical green as the entire chromatic budget; dark mode inverts to a near-black soil tone and lifts the green to a young-leaf tint.

### Primary

- **Pressed Fern** (`{colors.pressed-fern}`): The only chromatic color in light mode. It appears on the two 1.5rem rules flanking the role line, the botanical ornament, link icons on hover and focus, and the focus ring. Nowhere else.
- **New Growth** (`{colors.new-growth}`): The dark-mode counterpart, lifted in lightness so it holds contrast on the dark ground. Same four jobs, no more.

### Neutral

- **Warm Paper** (`{colors.paper}`): The page ground in light mode — a cream with a perceptible yellow cast, never `#fff`.
- **Soil Black** (`{colors.night-paper}`): The dark-mode ground. Warm and slightly green-black, not neutral charcoal.
- **Warm Ink** (`{colors.ink}`) / **Bone** (`{colors.night-ink}`): Primary text and link labels in the two themes.
- **Muted Ink** (`{colors.ink-muted}`) / **Weathered Bone** (`{colors.night-ink-muted}`): The role line, the description, section headings, expander label, and link icons at rest. The step down from primary text that carries most of the page's hierarchy.
- **Subtle Ink** (`{colors.ink-subtle}`) / **Faded Bone** (`{colors.night-ink-subtle}`): Dates and the footer stamp only — the quietest tier.
- **Rule** (`{colors.rule}`) / **Night Rule** (`{colors.night-rule}`): Every 1px border on the page: link rows, the mat, the expander, the inner hairline.
- **Hover Wash** (`{colors.surface-hover}`) / **Night Wash** (`{colors.night-surface-hover}`): The single-step background shift on hover and focus for link rows and the expander.
- **QR White** (`{colors.qr-white}`): The mat behind the QR code. Pure white, in both themes.

### Named Rules

**The One Green Rule.** Pressed Fern gets four jobs: the rules flanking the role, the ornament, icons on hover/focus, and the focus ring. It is never a fill, never a border color, never body text, never a link color at rest. Its rarity is what makes the page feel tended rather than branded.

**The Un-themed QR Rule.** The QR mat and code stay pure black on pure white in every theme. A phone camera in bad venue lighting outranks palette coherence. Do not add `prefers-color-scheme` overrides for `{colors.qr-white}`.

**The Warm Neutral Rule.** No neutral on this page is achromatic. Every gray carries the paper's yellow-warm cast. Dropping a `#888` or a `#f5f5f5` into this system reads instantly as foreign.

## Typography

**Display Font:** Petrona (with `ui-serif`, Georgia, serif)
**Body Font:** Hanken Grotesk (with `ui-sans-serif`, `system-ui`, sans-serif)
**Label Font:** Hanken Grotesk, uppercase and widely tracked — no third family

**Character:** Petrona is a warm humanist serif — wider and lower-contrast than an editorial display face, with terminals that read as drawn rather than drafted. It does not perform; it sits. That restraint is why it belongs on a page whose structure is entirely hairlines, and it is deliberately *not* a high-contrast fashion serif. Hanken Grotesk underneath is humanist and unfussy, so the serif never has to compete. Both are self-hosted woff2; Petrona ships at 400 only, Hanken Grotesk at 400 and 500. There is no 600, no 700, and no italic anywhere in the system.

The display step carries a **~4% size premium** over the rest of the scale (`clamp(2.0625rem → 2.875rem)` rather than `2rem → 2.75rem`). Petrona's x-height runs smaller than Hanken Grotesk's, so at an identical `font-size` the name would surrender presence to the body copy beneath it.

### Hierarchy

- **Display** (400, `clamp(2.0625rem → 2.875rem)`, 1.1, `-0.015em`): The name. This is the only Petrona on the page.
- **Title** (500, `clamp(0.875rem → 0.9375rem)`, `0.14em`, uppercase): The role line, centered and flanked by two 1.5rem × 1px green rules with a 0.75rem gap.
- **Body** (400, `clamp(1rem → 1.0625rem)`, 1.55, max 30rem): The description and every link label.
- **Label** (500, `clamp(0.75rem → 0.8125rem)`, `0.14em`, uppercase): The "Extras" section heading and the expander summary.
- **Meta** (400, same size as Label, `0.06em`, `tabular-nums`): Extra dates and the "Updated" footer stamp.

### Named Rules

**The Single Serif Rule.** Petrona appears exactly once per page, on the name. The moment a second element takes the serif, the name stops being the anchor. (The OG card is the one sanctioned exception: it sets both the name and the role line in Petrona, because a 1200×630 card has no hairline system to carry hierarchy.)

**The Tracked-Caps Rule.** Anything secondary — role, section heading, expander — is uppercase at `0.14em`. Never letterspace lowercase text, and never set body copy in caps.

**The Two-Weight Rule.** 400 and 500 are the entire weight vocabulary. Emphasis comes from size, case, tracking, and color tier — never from a heavier cut.

**The Tabular Date Rule.** Every date on the page is `font-variant-numeric: tabular-nums` at `0.06em`, so a stacked list of dates aligns down the column.

**Font pipeline note.** `src/fonts.py` self-hosts from Google Fonts, and Google picks the file format from **both** the User-Agent and the request shape. A pinned single weight (`Petrona:wght@400`) served to a Firefox UA comes back as `.woff`, which the script's woff2-only regex skips — leaving absolute `fonts.gstatic.com` URLs in `assets/fonts.css` and silently converting self-hosted fonts into a runtime third-party fetch. The script now sends a Chrome UA (woff2, and a static instance at roughly half the variable font's size) and hard-fails if any un-localized URL survives the rewrite. Two rules follow: after changing the request, confirm the new woff2 files actually landed in `assets/fonts/` and delete the orphaned ones; and any `font-variation-settings` axis must appear in the request URL or it does nothing at all.

## Layout

One centered column, `36rem` max width, on a body that is a flex container with `min-height: 100svh` and `1.5rem 1rem` padding — the page is centered horizontally but top-aligned, so short and long content behave the same.

The profile stack is a flex column with a uniform `1.5rem` gap: avatar, name, role, description, links. Link groups tighten to a `0.75rem` gap internally, which is what separates "these are siblings in a list" from "these are sections". The Extras section opens at `3rem` — the page's only large break — and the footer takes the same `3rem`. Description copy is capped at `30rem`, narrower than the container, so it never runs the full measure.

Spacing is a 4px geometric scale (`0.25 / 0.5 / 0.75 / 1 / 1.5 / 3rem`). Note the deliberate gap: there is no `2rem` step. Sections either breathe at `1.5rem` or break at `3rem`.

Two breakpoints, and only one of them is about width:

- **`max-width: 600px`** — the QR mat narrows from 512px to 320px so the code stays comfortably in thumb reach.
- **`(min-width: 640px) and (hover: hover) and (pointer: fine)`** — a capability query, not a size query. Pointer devices get the plain circular portrait; anything touch-capable keeps the scannable QR. The `<picture>` source and both `<link rel=preload>` tags use this exact query, so only one avatar is ever fetched.

**The Capability-Not-Width Rule.** The avatar switch is decided by `hover` and `pointer`, not by viewport alone. A phone held in landscape at 800px is still a phone, and it still gets the QR.

## Elevation & Depth

This system has no shadow vocabulary at all. There is not a single `box-shadow` in the stylesheet, and depth is drawn rather than lit: a 1px rule for every edge, a second hairline inset `0.5rem` inside the mat to create the only layered plane on the page, and a 1px `translateY` on `:active` that reads as pressing paper rather than lifting a card.

**The Drawn-Not-Lit Rule.** Flat is the default and shadows are a smell. If a future element genuinely needs to float above the sheet — a dialog, a lifted card — it may earn one, but it must be argued for, not reached for. Ambient shadows on resting surfaces are always wrong here.

## Shapes

Corners are `2px` — present enough that nothing looks brutalist, small enough that nothing reads as a component-library card. Link rows, the expander, and the focus ring all share it. The desktop portrait at `50%` is the only true circle in the system, and the QR mat is deliberately a hard rectangle: mats do not have rounded corners.

Borders are always exactly `1px solid` in the rule color, applied through a single `--rule` shorthand token so the whole page's line weight moves together. The recurring silhouette is a bordered rectangle in a vertical stack, punctuated once by the mat's double frame and once by the leaf.

**The 2px Rule.** `2px` or `50%`. Nothing in between — no `4px`, no `8px`, no `rounded-xl`.

## Components

### Link Rows

Specimen labels, not buttons. Each is a hairline-bordered row mounted in the column, holding an inlined SVG icon at `1.4em` and a label, with a `1rem` gap between them.

- **Shape:** Near-square corners (`{rounded.sm}`), `1px` rule border, `1rem 1.5rem` padding, `44px` minimum height for touch.
- **Rest:** Transparent ground, ink label, muted icon.
- **Hover / Focus:** Ground washes to the hover surface, border darkens to muted ink, and the icon greens to Pressed Fern. Three properties, 180ms, all on the same `cubic-bezier(0.2, 0.8, 0.2, 1)`.
- **Active:** `translateY(1px)`. The whole tactile budget in one line.
- **Extras variant:** Same row, with the label and a tabular date stacked in a `0.25rem` column beside the icon. The icon pins to the **first line** of the label (`align-items: flex-start` plus a half-leading nudge) rather than centering against the whole block — a three-line title would otherwise strand its icon down beside the date.

**The Greening Icon Rule.** The icon is the only thing that changes color on hover. It is the system's smallest, most-repeated moment of life; do not add a color change to the label too.

### Expander

The expander is a `<details>`/`<summary>` with its native marker removed. It borrows the link row's border, radius, hover wash, and hit target, but takes the tracked-caps Label voice at muted ink — so it reads as an instruction to the sheet, not another specimen on it. Its label answers its own state: "Show more (n)" when closed, "Show less" when open, swapped in CSS off the `[open]` attribute with no JavaScript.

**The Answering Label Rule.** A control's label states what the control will do next, never what it did. A toggle still reading "Show more" while its rows are open is a broken control, not a styling detail.

### Avatar Mat (signature)

The QR code sits on a pure-white ground with `1.5rem` of padding, a `1px` rule border, and a second `1px` hairline inset `0.5rem` via `::before`. On pointer devices the mat dissolves entirely — background to transparent, padding to zero, `border-radius: 50%` — and the border becomes a ring hugging the portrait. Same element, two different objects.

### Role Line (signature)

The title is a flex row whose `::before` and `::after` are `1.5rem × 1px` bars in the accent green, with a `0.75rem` gap. It is the only place a rule and the accent color meet, and it frames the role the way a specimen label frames a species name.

### Botanical Ornament (signature)

A 120×16 inline SVG: two horizontal lines with a hand-plotted leaf between them, drawn in `currentColor` at the accent green, stroke-width 1 with a 0.6 vein. It replaces the divider above the Extras section and is `aria-hidden`. This is the page's single decorative flourish, and it is load-bearing — it is what makes the sheet feel drawn.

### Focus

`2px solid` accent outline at `3px` offset with a `2px` radius, applied globally through `:focus-visible`. Keyboard focus is styled once, in the base layer, and every component inherits it.

## Do's and Don'ts

### Do:

- **Do** keep Pressed Fern to its four jobs — flanking rules, ornament, icon hover, focus ring. New accents belong nowhere.
- **Do** build depth with 1px rules in the `rule` color, and let `:active` `translateY(1px)` carry the tactility.
- **Do** compose any new section the same way the Extras section is composed: ornament, tracked-caps heading, then specimen rows.
- **Do** set every date with `tabular-nums` and `0.06em` tracking so columns of dates align.
- **Do** honor the `44px` minimum hit height on anything interactive — this page is used on phones, one-handed, standing up.
- **Do** route all motion through `--dur` / `--ease`, which `prefers-reduced-motion` already zeroes at the token level.
- **Do** self-host any new font or icon and inline it at build time; nothing on this page fetches from a third party at load.
- **Do** keep the QR mat pure black-on-white in every theme.

### Don't:

- **Don't** add a `box-shadow` to a resting surface. Flat is the default; a floating element must justify itself.
- **Don't** introduce a radius other than `2px` or `50%`.
- **Don't** set a second element on the page in Petrona, or add a weight beyond 400 and 500.
- **Don't** use an achromatic gray — every neutral here is warm.
- **Don't** letterspace lowercase text, or set body copy in uppercase.
- **Don't** drift toward the three rejected worlds: bio-link SaaS (pill buttons, gradients, candy cards), dev-portfolio dark neon (mono everything, glow, terminal green), or generic SaaS landing (rounded-xl, blue-500, Inter, drop shadows).
- **Don't** widen the column past `36rem` or run description copy past `30rem`.
- **Don't** swap the QR avatar out of the anchor position — it is the page's identity device and it circulates offline.
