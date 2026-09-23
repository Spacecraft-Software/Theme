# Installing Spacecraft Software Theme for MATE Desktop

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## What's here

Each theme in the Steelbore palette family (Standard §11) ships as a pair of
files under `themes/<slug>/`:

- `gtk.css` — MATE panel rules (menu bar, applets, clock/status icons) plus
  the GTK3 legacy colour names (`theme_bg_color`, `theme_selected_bg_color`,
  …) that Caja and MATE's other GTK3 applications resolve theme colour
  through.
- `metacity-theme-1.xml` — Metacity window-border geometry and colours
  (frame fill, border, title bar, title text), plus a `focused` frame style
  with an accent-coloured border.

`steelbore` is the default theme and the one to start with. Every dark theme
in the family (including `steelbore`) ships a `-high-contrast` sibling for
Standard §18 accessible mode. `steelbore-navywhite` is the family's light
theme, also with a `-high-contrast` sibling. `solarized-dark` /
`solarized-light` are a **fidelity palette** (Standard §11.5) — reproduced
verbatim from upstream Solarized for people who want it, but they are
**non-conforming** and not the recommended Spacecraft Software look.

Neither MATE's panel CSS nor Metacity has a per-file light/dark flag of its
own — MATE resolves light vs. dark from the desktop's own appearance
setting, not from anything a theme file declares. Pick `steelbore-navywhite`
for a light desktop; the files themselves work either way.

## Installation

### Panel theme (GTK3 / Caja)

1. Pick a theme slug, e.g. `steelbore` (or `steelbore-navywhite` for a light
   desktop, or a `-high-contrast` sibling for accessible mode).
2. Copy `themes/<slug>/gtk.css` to
   `~/.themes/Spacecraft-Software-<slug>/gtk-3.0/gtk.css`.
3. Open **System** → **Preferences** → **Appearance** → **Theme** and select
   the installed theme.

### Window Borders (Metacity)

1. Create the theme directory:
   ```sh
   mkdir -p ~/.themes/Spacecraft-Software-<slug>/metacity-1/
   ```
2. Copy `themes/<slug>/metacity-theme-1.xml` into it.
3. Open **System** → **Preferences** → **Appearance** → **Customize** →
   **Window Border** → select **Spacecraft-Software-\<slug\>**.

### Wallpaper

1. Copy `Spacecraft_Software_wallpaper_blue.png` to `~/Pictures/`.
2. Right-click desktop → **Change Desktop Background** → select the
   wallpaper.

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
