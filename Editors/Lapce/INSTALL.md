# Installing the Spacecraft Software themes for Lapce

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Lapce colour theme TOML file per registered theme of the
Steelbore palette family (The Steelbore Standard §11). `steelbore.toml` is the
default; every conforming palette also ships a `-high-contrast` sibling for
accessible mode. All files are generated from `Steelbore/steelbore.toml` — do
not edit them by hand.

## Installation

1. Copy the files from `themes/` into your Lapce themes directory:
   - **Linux:** `~/.config/lapce-stable/themes/`
   - **macOS:** `~/Library/Application Support/dev.lapce.Lapce-Stable/themes/`
   - **Windows:** `%APPDATA%\dev.lapce.Lapce-Stable\themes\`
2. Open Lapce → **Command Palette** (`Ctrl+Shift+P`) → **Change Color Theme**.
3. Select the theme you want — **Steelbore** is the default — from the list.

Each file's `[theme]` table names it exactly as it appears in that picker
(`name`, `color-theme.name`); `color-theme.type` is set from the theme's own
polarity, so `Steelbore NavyWhite` and `Solarized Light` register as light
themes and everything else as dark.

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.toml` | Steelbore Modern | **default** |
| `steelbore-high-contrast.toml` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.toml`, `steelbore-magnetar.toml`, `steelbore-biolume.toml`, `tokyonight.toml`, `steelbore-hanzosteel.toml`, `steelbore-blackpinkpanther.toml`, `steelbore-green.toml`, `steelbore-greenalt.toml` | alternates (§11.3) | each with a `-high-contrast.toml` sibling |
| `steelbore-navywhite.toml` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.toml` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.toml`, `solarized-light.toml` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |

Lapce's theme format is hex-only, so it cannot express the palette-independent
`steelbore-mono` theme; for `NO_COLOR` sessions leave Lapce on its own
defaults or pick a `-high-contrast` sibling instead.
