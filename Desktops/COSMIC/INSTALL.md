# Installing Spacecraft Software Theme for COSMIC Desktop

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Layout

Every theme is a generated COSMIC theme file at `themes/<slug>.ron`.
`steelbore` (Steelbore Modern, Void Navy) is the default; every conforming
palette ships a `-high-contrast` sibling for accessible mode (§18.1). The two
Solarized themes are a non-conforming **fidelity palette** (§11.5), shipped
for interoperability only — do not adopt them as a project palette. COSMIC's
`.ron` format is hex-only, so `steelbore-mono` (4-bit ANSI) is not shipped
here — use it on a terminal target instead.

| Slug | Theme |
|------|-------|
| `steelbore` | Steelbore (default) |
| `steelbore-high-contrast` | Steelbore High Contrast |
| `steelbore-blue`, `-high-contrast` | Steelbore Blue |
| `steelbore-magnetar`, `-high-contrast` | Steelbore Magnetar |
| `steelbore-biolume`, `-high-contrast` | Steelbore Biolume |
| `steelbore-navywhite`, `-high-contrast` | Steelbore NavyWhite (light canvas) |
| `tokyonight`, `-high-contrast` | Tokyo Night |
| `steelbore-hanzosteel`, `-high-contrast` | Steelbore Hanzo Steel |
| `steelbore-blackpinkpanther`, `-high-contrast` | Steelbore BlackPinkPanther |
| `steelbore-green`, `-high-contrast` | Steelbore Green |
| `steelbore-greenalt`, `-high-contrast` | Steelbore Green Alt |
| `steelbore-classic`, `-high-contrast` | Steelbore Classic (legacy six-role) |
| `solarized-dark`, `solarized-light` | Solarized — **fidelity, non-conforming** |

## Installation

### Theme

1. Copy the `.ron` file for the theme you want from `themes/` to:
   - `~/.config/cosmic/com.system76.CosmicTheme.Dark/v1/` for a dark theme
     (`is_dark: true`)
   - `~/.config/cosmic/com.system76.CosmicTheme.Light/v1/` for a light theme
     (`is_dark: false` — `steelbore-navywhite`, `solarized-light`)
2. Rename the copied file to `theme_builder_config.ron` (COSMIC reads one
   active config per mode directory), or keep the descriptive name if your
   COSMIC build supports theme selection by file.
3. Open **Settings** → **Desktop** → **Appearance** → select the Spacecraft
   Software theme.

Keep more than one `.ron` file cached outside those directories (e.g. leave
the rest under `themes/`) to switch later — just swap which one is copied in.

### Wallpaper

1. Copy `Spacecraft_Software_wallpaper_blue.png` to your wallpapers
   directory.
2. Set wallpaper via **Settings** → **Desktop** → **Wallpaper**.
