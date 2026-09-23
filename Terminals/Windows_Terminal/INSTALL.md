# Installing Spacecraft Software Theme for Windows Terminal

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Open Windows Terminal → **Settings** (or press `Ctrl+,`).
2. Click **Open JSON file** (bottom-left corner).
3. Copy the contents of `schemes.json` into the `"schemes"` array in your settings.json (or paste individual `themes/<slug>.json` files one at a time).
4. Under the profile you want to theme, set:
   ```json
   "colorScheme": "Steelbore"
   ```
   (or any other theme slug name).
5. Save and close the file. The theme is applied instantly.

## Available Themes

The generator produces 24 themes across 13 palettes (hex-only format — no mono/ANSI theme), all conforming to The Steelbore Standard §11 except where noted:

| Theme | Slug | Canvas | Conformance |
|-------|------|--------|-------------|
| **Steelbore** (default) | `steelbore` | Dark | Conforming |
| Steelbore High Contrast | `steelbore-high-contrast` | Dark | Conforming (accessible) |
| Steelbore Blue | `steelbore-blue` | Dark | Conforming |
| Steelbore Blue High Contrast | `steelbore-blue-high-contrast` | Dark | Conforming |
| Steelbore Magnetar | `steelbore-magnetar` | Dark | Conforming |
| Steelbore Magnetar High Contrast | `steelbore-magnetar-high-contrast` | Dark | Conforming |
| Steelbore Biolume | `steelbore-biolume` | Dark | Conforming |
| Steelbore Biolume High Contrast | `steelbore-biolume-high-contrast` | Dark | Conforming |
| Steelbore NavyWhite | `steelbore-navywhite` | Light | Conforming |
| Steelbore NavyWhite High Contrast | `steelbore-navywhite-high-contrast` | Light | Conforming |
| Tokyo Night | `tokyonight` | Dark | Conforming |
| Tokyo Night High Contrast | `tokyonight-high-contrast` | Dark | Conforming |
| Steelbore Hanzo Steel | `steelbore-hanzosteel` | Dark | Conforming |
| Steelbore Hanzo Steel High Contrast | `steelbore-hanzosteel-high-contrast` | Dark | Conforming |
| Steelbore BlackPinkPanther | `steelbore-blackpinkpanther` | Dark | Conforming |
| Steelbore BlackPinkPanther High Contrast | `steelbore-blackpinkpanther-high-contrast` | Dark | Conforming |
| Steelbore Green | `steelbore-green` | Dark | Conforming |
| Steelbore Green High Contrast | `steelbore-green-high-contrast` | Dark | Conforming |
| Steelbore Green Alt | `steelbore-greenalt` | Dark | Conforming |
| Steelbore Green Alt High Contrast | `steelbore-greenalt-high-contrast` | Dark | Conforming |
| Steelbore Classic | `steelbore-classic` | Dark | Legacy (6-role) |
| Steelbore Classic High Contrast | `steelbore-classic-high-contrast` | Dark | Legacy |
| Solarized Dark | `solarized-dark` | Dark | **Fidelity (non-conforming)** |
| Solarized Light | `solarized-light` | Light | **Fidelity (non-conforming)** |

**Note:** Solarized themes are fidelity palettes reproduced verbatim from the original Solarized project and are not adoptable as project themes.

## Environment Variable

On supported shells and terminal multiplexers, set `SPACECRAFT_THEME=<slug>` to switch themes programmatically.
