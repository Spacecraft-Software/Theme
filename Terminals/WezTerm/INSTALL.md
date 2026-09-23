# Installing Spacecraft Software Themes for WezTerm

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy the entire `themes/` directory to your WezTerm colors directory:
   ```sh
   cp themes/* ~/.config/wezterm/colors/
   ```
   This installs all 24 Spacecraft Software themes (one `.lua` file per theme).

2. In your `~/.config/wezterm/wezterm.lua`, configure your preferred theme:
   ```lua
   config.color_scheme = "steelbore"  -- or any theme slug from the table below
   ```

3. Save and WezTerm will reload automatically.

## Choosing a Theme

The Spacecraft Software palette family (v3.5.0, The Steelbore Standard §11) is reproduced across 24 color schemes, organized by palette and variant:

| Theme Slug | Name | Variant | Canvas |
|---|---|---|---|
| **`steelbore`** | Steelbore | **Default (Modern)** | Dark |
| `steelbore-high-contrast` | Steelbore High Contrast | Accessible variant | Dark |
| `steelbore-blue` | Steelbore Blue | Alternate palette | Dark |
| `steelbore-blue-high-contrast` | Steelbore Blue High Contrast | Alternate variant | Dark |
| `steelbore-magnetar` | Steelbore Magnetar | Alternate palette | Dark |
| `steelbore-magnetar-high-contrast` | Steelbore Magnetar High Contrast | Alternate variant | Dark |
| `steelbore-biolume` | Steelbore Biolume | Alternate palette | Dark |
| `steelbore-biolume-high-contrast` | Steelbore Biolume High Contrast | Alternate variant | Dark |
| `steelbore-navywhite` | Steelbore NavyWhite | Alternate palette | **Light** |
| `steelbore-navywhite-high-contrast` | Steelbore NavyWhite High Contrast | Alternate variant | **Light** |
| `tokyonight` | Tokyo Night | Alternate palette | Dark |
| `tokyonight-high-contrast` | Tokyo Night High Contrast | Alternate variant | Dark |
| `steelbore-hanzosteel` | Steelbore Hanzo Steel | Alternate palette | Dark |
| `steelbore-hanzosteel-high-contrast` | Steelbore Hanzo Steel High Contrast | Alternate variant | Dark |
| `steelbore-blackpinkpanther` | Steelbore BlackPinkPanther | Alternate palette | Dark |
| `steelbore-blackpinkpanther-high-contrast` | Steelbore BlackPinkPanther High Contrast | Alternate variant | Dark |
| `steelbore-green` | Steelbore Green | Alternate palette | Dark |
| `steelbore-green-high-contrast` | Steelbore Green High Contrast | Alternate variant | Dark |
| `steelbore-greenalt` | Steelbore Green Alt | Alternate palette | Dark |
| `steelbore-greenalt-high-contrast` | Steelbore Green Alt High Contrast | Alternate variant | Dark |
| `steelbore-classic` | Steelbore Classic | Legacy six-role palette | Dark |
| `solarized-dark` | Solarized Dark | *Non-conforming fidelity* | Dark |
| `solarized-light` | Solarized Light | *Non-conforming fidelity* | Light |

All conforming Steelbore themes (variants other than Solarized) are WCAG 2.2 AA verified. Each palette includes a `-high-contrast` accessible variant with lifted accent colours. Solarized themes are reproduced verbatim for compatibility and are not adoptable as project palettes (fidelity mode, §11.5).

### Environment Variable

Alternatively, set `SPACECRAFT_THEME=<slug>` and configure WezTerm to read it:
```lua
local theme_env = os.getenv("SPACECRAFT_THEME") or "steelbore"
config.color_scheme = theme_env
```
