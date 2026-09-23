# Installing Spacecraft Software Theme for XFCE

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

The XFCE GTK CSS themes are distributed as directories under `themes/`, one per palette variant. Each directory contains a single `gtk.css` file.

### Installing a Theme

1. Choose your theme from the available options below.
2. Copy the desired theme directory to your XFCE themes folder:
   ```bash
   cp -r themes/<slug> ~/.themes/Spacecraft-Software
   ```
3. Open **Settings** → **Appearance** → **Style** and select the theme.
4. Alternatively, you can copy only the `gtk.css` file:
   ```bash
   mkdir -p ~/.themes/Spacecraft-Software/gtk-3.0
   cp themes/<slug>/gtk.css ~/.themes/Spacecraft-Software/gtk-3.0/gtk.css
   ```

### Choosing a Theme

| Theme | Slug | Description | Polarity |
|-------|------|-------------|----------|
| **Steelbore** (recommended) | `steelbore` | Default palette, modern aesthetic | Dark |
| Steelbore High Contrast | `steelbore-high-contrast` | Accessible variant with lifted contrast (§11.1.1) | Dark |
| Steelbore Blue | `steelbore-blue` | Electric blue accent variant | Dark |
| Steelbore Blue High Contrast | `steelbore-blue-high-contrast` | Accessible electric blue variant | Dark |
| Steelbore Magnetar | `steelbore-magnetar` | Bright orange-red accent palette | Dark |
| Steelbore Magnetar High Contrast | `steelbore-magnetar-high-contrast` | Accessible magnetar variant | Dark |
| Steelbore Biolume | `steelbore-biolume` | Vibrant cyan and green accents | Dark |
| Steelbore Biolume High Contrast | `steelbore-biolume-high-contrast` | Accessible biolume variant | Dark |
| **Steelbore NavyWhite** | `steelbore-navywhite` | Light theme with Void Navy as accent | Light |
| Steelbore NavyWhite High Contrast | `steelbore-navywhite-high-contrast` | Accessible light variant | Light |
| Tokyo Night | `tokyonight` | Japanese anime-inspired dark palette | Dark |
| Tokyo Night High Contrast | `tokyonight-high-contrast` | Accessible Tokyo Night variant | Dark |
| Steelbore Hanzo Steel | `steelbore-hanzosteel` | Stealth-inspired metallic palette | Dark |
| Steelbore Hanzo Steel High Contrast | `steelbore-hanzosteel-high-contrast` | Accessible Hanzo Steel variant | Dark |
| Steelbore BlackPinkPanther | `steelbore-blackpinkpanther` | Bold black and pink palette | Dark |
| Steelbore BlackPinkPanther High Contrast | `steelbore-blackpinkpanther-high-contrast` | Accessible BlackPinkPanther variant | Dark |
| Steelbore Green | `steelbore-green` | Nature-inspired green palette | Dark |
| Steelbore Green High Contrast | `steelbore-green-high-contrast` | Accessible green variant | Dark |
| Steelbore Green Alt | `steelbore-greenalt` | Alternative green palette variant | Dark |
| Steelbore Green Alt High Contrast | `steelbore-greenalt-high-contrast` | Accessible green alt variant | Dark |
| Steelbore Classic | `steelbore-classic` | Legacy six-role contract (§11.2) | Dark |
| Steelbore Classic High Contrast | `steelbore-classic-high-contrast` | Accessible classic variant | Dark |
| Solarized Dark | `solarized-dark` | Fidelity palette (non-conforming, §11.5) | Dark |
| Solarized Light | `solarized-light` | Fidelity palette (non-conforming, §11.5) | Light |

**Note:** The Solarized themes are non-conforming fidelity palettes (§11.5) reproduced verbatim and are not adoptable as project palettes.

### Wallpaper

1. Copy `Spacecraft_Software_wallpaper_blue.png` to `~/Pictures/` if available.
2. Right-click desktop → **Desktop Settings** → select the wallpaper.

### XFCE Terminal

See the XFCE Terminal theme installation guide for terminal color scheme configuration.
