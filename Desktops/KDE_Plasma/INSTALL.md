# Installing Spacecraft Software Theme for KDE Plasma

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Layout

Every theme is a generated KDE colour scheme at `themes/<slug>.colors`.
`steelbore` (Steelbore Modern, Void Navy) is the default; every conforming
palette ships a `-high-contrast` sibling for accessible mode (§18.1). The two
Solarized themes are a non-conforming **fidelity palette** (§11.5), shipped
for interoperability only — do not adopt them as a project palette.

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

### Colour scheme

1. Copy the `.colors` file for the theme you want from `themes/` to:
   - `~/.local/share/color-schemes/`
2. Open **System Settings** → **Appearance** → **Colors** → select the theme
   by its display name (e.g. **Steelbore**, **Steelbore NavyWhite**).

Install more than one file to switch between themes later from the same
Colors page — each `.colors` file is self-contained.

### Wallpaper

1. Copy `Spacecraft_Software_wallpaper_blue.png` to `~/Pictures/`.
2. Right-click desktop → **Configure Desktop** → select the wallpaper.

### Konsole terminal

See `Theme/Terminals/Konsole/INSTALL.md` for the matching terminal colour
scheme — install the same slug on both surfaces for a consistent look.
