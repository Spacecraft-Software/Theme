# Installing Spacecraft Software Theme for Ghostty

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy a theme file to your Ghostty config directory:
   - **Linux:** `~/.config/ghostty/themes/`
   - **macOS:** `~/Library/Application Support/com.mitchellh.ghostty/themes/`

2. In your Ghostty config (`~/.config/ghostty/config` or equivalent), set:
   ```
   theme = <theme-name>
   ```

3. Restart Ghostty or reload the config with `Ctrl+Shift+,`.

## Available Themes

Each theme file is located in the `themes/` directory of this distribution. The **default theme** is `steelbore` (modern design with Void Navy canvas and Molten Amber accents).

| Theme Slug | Name | Polarity | Notes |
|-----------|------|----------|-------|
| `steelbore` | Steelbore | Dark | Default theme, standard conformance |
| `steelbore-high-contrast` | Steelbore High Contrast | Dark | Accessible variant with enhanced contrast |
| `steelbore-blue` | Steelbore Blue | Dark | Blue-accented variant |
| `steelbore-blue-high-contrast` | Steelbore Blue High Contrast | Dark | Blue variant, high contrast |
| `steelbore-magnetar` | Steelbore Magnetar | Dark | Magenta-accented variant |
| `steelbore-magnetar-high-contrast` | Steelbore Magnetar High Contrast | Dark | Magnetar variant, high contrast |
| `steelbore-biolume` | Steelbore Biolume | Dark | Bioluminescent variant |
| `steelbore-biolume-high-contrast` | Steelbore Biolume High Contrast | Dark | Biolume variant, high contrast |
| `steelbore-navywhite` | Steelbore NavyWhite | Light | Light canvas variant |
| `steelbore-navywhite-high-contrast` | Steelbore NavyWhite High Contrast | Light | NavyWhite variant, high contrast |
| `tokyonight` | Tokyo Night | Dark | Tokyo Night variant |
| `tokyonight-high-contrast` | Tokyo Night High Contrast | Dark | Tokyo Night variant, high contrast |
| `steelbore-hanzosteel` | Steelbore Hanzo Steel | Dark | Hanzo Steel variant |
| `steelbore-hanzosteel-high-contrast` | Steelbore Hanzo Steel High Contrast | Dark | Hanzo Steel variant, high contrast |
| `steelbore-blackpinkpanther` | Steelbore BlackPinkPanther | Dark | BlackPinkPanther variant |
| `steelbore-blackpinkpanther-high-contrast` | Steelbore BlackPinkPanther High Contrast | Dark | BlackPinkPanther variant, high contrast |
| `steelbore-green` | Steelbore Green | Dark | Green-accented variant |
| `steelbore-green-high-contrast` | Steelbore Green High Contrast | Dark | Green variant, high contrast |
| `steelbore-greenalt` | Steelbore Green Alt | Dark | Alternative green variant |
| `steelbore-greenalt-high-contrast` | Steelbore Green Alt High Contrast | Dark | Green Alt variant, high contrast |
| `steelbore-classic` | Steelbore Classic | Dark | Legacy six-role contract variant |
| `solarized-dark` | Solarized Dark | Dark | Fidelity palette (non-conforming) |
| `solarized-light` | Solarized Light | Light | Fidelity palette (non-conforming, light) |

**Note:** The Solarized variants are reproduced verbatim from their upstream project and are **not adoptable as a project palette** (§11.5, fidelity category). Use Steelbore variants for projects adopting this theme system.

## Environment Variable

Set the `SPACECRAFT_THEME` environment variable to specify a default theme across compatible Spacecraft Software applications:

```bash
export SPACECRAFT_THEME=steelbore-high-contrast
```

Ghostty will use the theme specified in its config file if set; the environment variable serves other Spacecraft Software tools.
