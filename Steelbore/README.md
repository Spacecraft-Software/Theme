# Steelbore — the palette family registry

**Canonical Spacecraft Software colour contract — The Steelbore Standard §11 (v2.08), palette family v3.5.0**

This directory is the single source of colour for the whole repository.

| File | What it is |
|------|------------|
| `steelbore.toml` | Verbatim copy of the `steelbore-color-palette` skill's `assets/steelbore.toml`: thirteen palettes, twenty-five themes, measured WCAG 2.2 contrast matrices, per-palette rules, the §11.6 resolution tables and §12 typography. **Edit upstream, then copy here.** |
| `steelbore.json` | Generated JSON registry of every theme — name, palette, variant, polarity, conformance, the eleven role hexes, the derived ANSI-16 list and the measured contrast against the canvas. Regenerate with `cd tools && python3 -m steelbore_themes registry`. |
| `steelbore.css` | Generated CSS: the default theme's tokens on `:root`, one `[data-theme="<slug>"]` block per theme, and a `prefers-color-scheme: light` fallback to the family's light palette. |
| `themes/<slug>.css` | Generated per-theme CSS token files (`--steelbore-<role>`). |

Every other theme file in this repository is rendered from `steelbore.toml` by
`tools/steelbore_themes` — see `tools/README.md`.

---

## The family

| Slug | Palette | Canvas | Status |
|------|---------|--------|--------|
| `steelbore` | Steelbore Modern | Void Navy | **default** |
| `steelbore-classic` | Steelbore Classic | Void Navy | legacy six-role contract (§11.2) — the original Molten Amber look |
| `steelbore-blue` | Steelbore Blue | Orbit Navy | alternate (§11.3.1); accent is large-text/non-text only |
| `steelbore-magnetar` | Steelbore Magnetar | Core Black | alternate (§11.3.2) |
| `steelbore-biolume` | Steelbore Biolume | Circuit Navy | alternate (§11.3.3) |
| `steelbore-navywhite` | Steelbore NavyWhite | Pearl Silver | alternate (§11.3.4) — **light** |
| `tokyonight` | Tokyo Night | Night | alternate (§11.3.5), upstream verbatim |
| `steelbore-hanzosteel` | Steelbore Hanzo Steel | Sumi Black | alternate (§11.3.6) |
| `steelbore-blackpinkpanther` | Steelbore BlackPinkPanther | Runway Black | alternate (§11.3.7) — slug reused at v2.08 |
| `steelbore-green` | Steelbore Green | Vampire Black | alternate (§11.3.8), Erin is the foreground |
| `steelbore-greenalt` | Steelbore Green Alt | Vampire Black | alternate (§11.3.9), neutral foreground |
| `solarized-dark`, `solarized-light` | Solarized | base03 / base3 | **fidelity (§11.5) — non-conforming, not adoptable** |

Every conforming palette (and Classic) has a `<slug>-high-contrast` sibling
(§11.1.1) that lifts only the tokens below 7:1 on its canvas; the palette's
canvas never changes. `steelbore-mono` is the palette-independent 4-bit ANSI
theme for `NO_COLOR` and is emitted only by targets that take ANSI names.

## Role tokens (§11.1)

`background` · `surface` · `surface-alt` · `foreground` · `accent` ·
`structure` · `success` · `error` · `warning` · `focus` · `border`

Surface tokens are fills, never text. Classic binds the legacy six roles
(`background`, `foreground`, `accent`, `success`, `error`, `info`).

## How to use

- **Applications** register the theme under the name `steelbore` and reference
  role tokens, never hexes (§11.1). Parse `steelbore.toml` or `steelbore.json`.
- **Resolution** (§11.6): in-app selection → `SPACECRAFT_THEME=<slug>` →
  `$XDG_CONFIG_HOME/steelbore/theme.toml` / `/etc/steelbore/theme.toml` →
  platform light/dark preference → the project's declared palette (`steelbore`).
  A light preference resolves to `steelbore-navywhite` via
  `[resolution.pair]`.
- **Web**: `<link rel="stylesheet" href="steelbore.css">` and set
  `data-theme="<slug>"` on `<html>`.

> Hard-coding palette hex values directly in UI logic is **forbidden** for new
> Spacecraft Software apps. Use theme tokens exclusively. — The Steelbore Standard §11.1

See <https://Standard.SpacecraftSoftware.org/> for the normative text.

---

**License:** GPL-3.0-or-later (`steelbore.toml`, `steelbore.json`, CSS); this README CC-BY-SA-4.0
**Copyright:** Copyright (C) 2026 Mohamed Hammad & Spacecraft Software
