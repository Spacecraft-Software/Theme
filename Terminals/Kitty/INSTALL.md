# Installing the Spacecraft Software themes for Kitty

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Kitty colour file per registered theme of the Steelbore
palette family (The Steelbore Standard §11). `steelbore.conf` is the default;
every conforming palette also ships a `-high-contrast` sibling for accessible
mode. All files are generated from `Steelbore/steelbore.toml` — do not edit them.

## Installation

1. Copy the `themes/` directory into your Kitty config directory:
   `~/.config/kitty/themes/`
2. In `~/.config/kitty/kitty.conf`, include the theme you want:
   ```
   include themes/steelbore.conf
   ```
3. Reload Kitty (`Ctrl+Shift+F5`).

To follow the system-wide theme declaration (§11.6), point the include at the
slug carried by `SPACECRAFT_THEME`, for example from a launcher:
`kitty --override "include=themes/${SPACECRAFT_THEME:-steelbore}.conf"`.

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.conf` | Steelbore Modern | **default** |
| `steelbore-high-contrast.conf` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.conf`, `steelbore-magnetar.conf`, `steelbore-biolume.conf`, `tokyonight.conf`, `steelbore-hanzosteel.conf`, `steelbore-blackpinkpanther.conf`, `steelbore-green.conf`, `steelbore-greenalt.conf` | alternates (§11.3) | each with a `-high-contrast.conf` sibling |
| `steelbore-navywhite.conf` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.conf` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.conf`, `solarized-light.conf` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |

Kitty cannot express the palette-independent `steelbore-mono` theme; for
`NO_COLOR` sessions leave Kitty on its own defaults.
