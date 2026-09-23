# Installing the Spacecraft Software themes for Zamak

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Zamak colour file per registered theme of the Steelbore palette family (The Steelbore Standard §11). `steelbore.toml` is the default; every conforming palette also ships a `-high-contrast` sibling for accessible mode. All files are generated from `Steelbore/steelbore.toml` — do not edit them.

## Installation

1. Copy the desired `themes/<slug>.toml` file to your Zamak configuration directory (typically `/boot/zamak/` or your bootloader's config path)
2. Reference the theme in your Zamak boot configuration
3. Reload or restart your bootloader to apply the new theme

To follow the system-wide theme declaration (§11.6), read the slug from `SPACECRAFT_THEME` environment variable, defaulting to `steelbore` if not set.

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.toml` | Steelbore Modern | **default** |
| `steelbore-high-contrast.toml` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.toml`, `steelbore-magnetar.toml`, `steelbore-biolume.toml`, `tokyonight.toml`, `steelbore-hanzosteel.toml`, `steelbore-blackpinkpanther.toml`, `steelbore-green.toml`, `steelbore-greenalt.toml` | alternates (§11.3) | each with a `-high-contrast.toml` sibling |
| `steelbore-navywhite.toml` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.toml` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.toml`, `solarized-light.toml` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |

Zamak cannot express the palette-independent `steelbore-mono` theme; bootloaders require explicit hex colour definitions.
