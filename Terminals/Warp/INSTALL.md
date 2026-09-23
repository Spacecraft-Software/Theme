# Installing Spacecraft Software Themes for Warp Terminal

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy any theme file from `themes/` to:
   - **macOS:** `~/.warp/themes/`
   - **Linux:** `~/.warp/themes/`
2. Open Warp → **Settings** → **Appearance** → **Themes** and select your chosen theme.

## Available Themes

The Spacecraft Software theme distribution includes 24 color themes. All are WCAG 2.2 AA verified unless otherwise noted.

| Theme | Slug | Canvas | Purpose |
|-------|------|--------|---------|
| **Steelbore** (default) | `steelbore` | Dark | Modern design palette, primary accent |
| Steelbore High Contrast | `steelbore-high-contrast` | Dark | Accessible variant of Steelbore |
| Steelbore Blue | `steelbore-blue` | Dark | Alternate palette with electric blue accent |
| Steelbore Blue High Contrast | `steelbore-blue-high-contrast` | Dark | Accessible variant |
| Steelbore Magnetar | `steelbore-magnetar` | Dark | High-energy accent variant |
| Steelbore Magnetar High Contrast | `steelbore-magnetar-high-contrast` | Dark | Accessible variant |
| Steelbore Biolume | `steelbore-biolume` | Dark | Vibrant, biotech-inspired palette |
| Steelbore Biolume High Contrast | `steelbore-biolume-high-contrast` | Dark | Accessible variant |
| Steelbore NavyWhite | `steelbore-navywhite` | **Light** | Light canvas with Navy accents |
| Steelbore NavyWhite High Contrast | `steelbore-navywhite-high-contrast` | **Light** | Accessible variant |
| Tokyo Night | `tokyonight` | Dark | Alternate palette, vibrant neon |
| Tokyo Night High Contrast | `tokyonight-high-contrast` | Dark | Accessible variant |
| Steelbore Hanzo Steel | `steelbore-hanzosteel` | Dark | Minimalist stealth palette |
| Steelbore Hanzo Steel High Contrast | `steelbore-hanzosteel-high-contrast` | Dark | Accessible variant |
| Steelbore BlackPinkPanther | `steelbore-blackpinkpanther` | Dark | High-contrast dark + magenta accent |
| Steelbore BlackPinkPanther High Contrast | `steelbore-blackpinkpanther-high-contrast` | Dark | Accessible variant |
| Steelbore Green | `steelbore-green` | Dark | Green accent variant |
| Steelbore Green High Contrast | `steelbore-green-high-contrast` | Dark | Accessible variant |
| Steelbore Green Alt | `steelbore-greenalt` | Dark | Alternative green palette |
| Steelbore Green Alt High Contrast | `steelbore-greenalt-high-contrast` | Dark | Accessible variant |
| Steelbore Classic | `steelbore-classic` | Dark | Legacy six-role contract (§11.2) |
| Steelbore Classic High Contrast | `steelbore-classic-high-contrast` | Dark | Accessible variant of Classic |
| Solarized Dark | `solarized-dark` | Dark | **Fidelity palette** — non-conforming reproduction |
| Solarized Light | `solarized-light` | **Light** | **Fidelity palette** — non-conforming reproduction |

**Note:** Solarized themes are reproduced verbatim from the Solarized project and are not conforming Spacecraft Software palettes. They are provided for compatibility and do not follow the Standard §11 color contract.

## Choosing a Theme

- **Steelbore** (default) is the recommended theme for everyday use
- High-contrast variants offer improved contrast for accessibility
- NavyWhite provides a **light canvas** option
- Use the `SPACECRAFT_THEME=<slug>` environment variable to set a default theme in Warp configuration
