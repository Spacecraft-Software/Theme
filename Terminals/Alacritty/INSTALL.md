# Installing Spacecraft Software Themes for Alacritty

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

Each theme is a separate `.toml` file. Copy the theme file(s) to your Alacritty configuration directory:

- **Linux/macOS:** `~/.config/alacritty/themes/`
- **Windows:** `%APPDATA%\alacritty\themes\`

Then in your main `alacritty.toml` configuration file, add an import statement. For example, to use the default **Steelbore** theme:

```toml
import = ["~/.config/alacritty/themes/steelbore.toml"]
```

Alternatively, set the `SPACECRAFT_THEME` environment variable (if your shell/terminal supports it) to select a theme:

```bash
export SPACECRAFT_THEME=steelbore-blue
```

## Available Themes

| Theme | Slug | Canvas | Variant |
|-------|------|--------|---------|
| **Steelbore** | `steelbore` | Dark | Default (Modern) |
| Steelbore High Contrast | `steelbore-high-contrast` | Dark | Accessible Mode |
| Steelbore Blue | `steelbore-blue` | Dark | Alternate |
| Steelbore Blue High Contrast | `steelbore-blue-high-contrast` | Dark | Accessible Mode |
| Steelbore Magnetar | `steelbore-magnetar` | Dark | Alternate |
| Steelbore Magnetar High Contrast | `steelbore-magnetar-high-contrast` | Dark | Accessible Mode |
| Steelbore Biolume | `steelbore-biolume` | Dark | Alternate |
| Steelbore Biolume High Contrast | `steelbore-biolume-high-contrast` | Dark | Accessible Mode |
| Steelbore NavyWhite | `steelbore-navywhite` | Light | Alternate |
| Steelbore NavyWhite High Contrast | `steelbore-navywhite-high-contrast` | Light | Accessible Mode |
| Tokyo Night | `tokyonight` | Dark | Alternate |
| Tokyo Night High Contrast | `tokyonight-high-contrast` | Dark | Accessible Mode |
| Steelbore Hanzo Steel | `steelbore-hanzosteel` | Dark | Alternate |
| Steelbore Hanzo Steel High Contrast | `steelbore-hanzosteel-high-contrast` | Dark | Accessible Mode |
| Steelbore BlackPinkPanther | `steelbore-blackpinkpanther` | Dark | Alternate |
| Steelbore BlackPinkPanther High Contrast | `steelbore-blackpinkpanther-high-contrast` | Dark | Accessible Mode |
| Steelbore Green | `steelbore-green` | Dark | Alternate |
| Steelbore Green High Contrast | `steelbore-green-high-contrast` | Dark | Accessible Mode |
| Steelbore Green Alt | `steelbore-greenalt` | Dark | Alternate |
| Steelbore Green Alt High Contrast | `steelbore-greenalt-high-contrast` | Dark | Accessible Mode |
| Steelbore Classic | `steelbore-classic` | Dark | Legacy (6-role) |
| Steelbore Classic High Contrast | `steelbore-classic-high-contrast` | Dark | Accessible Mode |
| Solarized Dark | `solarized-dark` | Dark | Non-conforming fidelity |
| Solarized Light | `solarized-light` | Light | Non-conforming fidelity |

**Note:** Solarized themes are provided for fidelity compatibility (§11.5) but are non-conforming to the Spacecraft Software palette contract and should not be adopted as project palettes.

## Reloading Themes

Alacritty >= 0.13 supports live configuration reloading. When you change the `import` statement in your configuration, Alacritty will automatically reload the theme when you focus the window (if `live_config_reload` is enabled).
