# Installing Spacecraft Software Theme for GNOME

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## What's here

Each theme in the Steelbore palette family (Standard §11) ships as a pair of
files under `themes/<slug>/`:

- `gtk.css` — libadwaita/GTK4 colour tokens (`@define-color`), plus the GTK3
  legacy colour names for older applications.
- `gnome-shell.css` — GNOME Shell chrome (top panel, popup menus, calendar).

`steelbore` is the default theme and the one to start with. Every dark theme
in the family (including `steelbore`) ships a `-high-contrast` sibling for
Standard §18 accessible mode. `steelbore-navywhite` is the family's light
theme, also with a `-high-contrast` sibling. `solarized-dark` /
`solarized-light` are a **fidelity palette** (Standard §11.5) — reproduced
verbatim from upstream Solarized for people who want it, but they are
**non-conforming** and not the recommended Spacecraft Software look.

GTK/libadwaita has no per-stylesheet light/dark flag of its own — GNOME
resolves light vs. dark from the `org.gnome.desktop.interface color-scheme`
desktop portal setting, not from anything a theme's CSS declares. Pick
`steelbore-navywhite` for a light desktop and pair it with a light
`color-scheme` setting; the CSS itself works either way.

## Installation

### GTK/Shell theme

1. Pick a theme slug, e.g. `steelbore` (or `steelbore-navywhite` for a light
   desktop, or a `-high-contrast` sibling for accessible mode).
2. Copy both files from `themes/<slug>/` to:
   - `~/.themes/Spacecraft-Software-<slug>/gtk-4.0/gtk.css`
   - `~/.themes/Spacecraft-Software-<slug>/gnome-shell/gnome-shell.css`
3. Use GNOME Tweaks or Extensions to select the installed shell theme.

### Wallpaper

1. Copy `Spacecraft_Software_wallpaper_blue.png` to `~/Pictures/`.
2. Right-click desktop → **Change Background** → select the wallpaper.

### GNOME Terminal

See `Theme/Terminals/GNOME_Terminal/INSTALL.md` for terminal color scheme.

## Choosing a theme

| Slug | Canvas | Notes |
|------|--------|-------|
| `steelbore` | dark | Default — Steelbore Modern |
| `steelbore-high-contrast` | dark | §11.1.1 accessible-mode sibling |
| `steelbore-navywhite` | light | Light canvas |
| `steelbore-navywhite-high-contrast` | light | Light, accessible-mode sibling |
| `steelbore-blue`, `-magnetar`, `-biolume`, `-hanzosteel`, `-blackpinkpanther`, `-green`, `-greenalt`, `tokyonight` | dark | Alternate palettes (§11.3), each with a `-high-contrast` sibling |
| `steelbore-classic`, `-high-contrast` | dark | Legacy six-role contract (§11.2) |
| `solarized-dark` / `solarized-light` | dark / light | Fidelity palette (§11.5) — non-conforming |

All themes are generated from `Steelbore/steelbore.toml`; do not hand-edit a
file under `themes/` — edit the palette source and regenerate.
