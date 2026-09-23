# Installing Spacecraft Software Themes for LeftWM

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Theme Files

Generated themes ship as `themes/<slug>/theme.toml` and `themes/<slug>/polybar.config` pairs. Each theme is standalone and can be installed independently:

- **`steelbore/`** — Steelbore (default, modern, dark)
- **`steelbore-high-contrast/`** — Steelbore High Contrast (accessible mode sibling, dark)
- **`steelbore-blue/`** — Steelbore Blue (alternate palette, dark)
- **`steelbore-blue-high-contrast/`** — Steelbore Blue High Contrast (dark)
- **`steelbore-magnetar/`** — Steelbore Magnetar (alternate palette, dark)
- **`steelbore-magnetar-high-contrast/`** — Steelbore Magnetar High Contrast (dark)
- **`steelbore-biolume/`** — Steelbore Biolume (alternate palette, dark)
- **`steelbore-biolume-high-contrast/`** — Steelbore Biolume High Contrast (dark)
- **`steelbore-navywhite/`** — Steelbore NavyWhite (light canvas, accessible)
- **`steelbore-navywhite-high-contrast/`** — Steelbore NavyWhite High Contrast (light canvas)
- **`tokyonight/`** — Tokyo Night (alternate palette, dark)
- **`tokyonight-high-contrast/`** — Tokyo Night High Contrast (dark)
- **`steelbore-hanzosteel/`** — Steelbore Hanzo Steel (alternate palette, dark)
- **`steelbore-hanzosteel-high-contrast/`** — Steelbore Hanzo Steel High Contrast (dark)
- **`steelbore-blackpinkpanther/`** — Steelbore BlackPinkPanther (alternate palette, dark)
- **`steelbore-blackpinkpanther-high-contrast/`** — Steelbore BlackPinkPanther High Contrast (dark)
- **`steelbore-green/`** — Steelbore Green (alternate palette, dark)
- **`steelbore-green-high-contrast/`** — Steelbore Green High Contrast (dark)
- **`steelbore-greenalt/`** — Steelbore Green Alt (alternate palette, dark)
- **`steelbore-greenalt-high-contrast/`** — Steelbore Green Alt High Contrast (dark)
- **`steelbore-classic/`** — Steelbore Classic (legacy six-role contract, dark)
- **`steelbore-classic-high-contrast/`** — Steelbore Classic High Contrast (dark)
- **`solarized-dark/`** — Solarized Dark (fidelity palette, non-conforming, dark)
- **`solarized-light/`** — Solarized Light (fidelity palette, non-conforming, light)

## Installation

**For the default theme (Steelbore):**

1. Copy `themes/steelbore/theme.toml` and `themes/steelbore/polybar.config` to:
   - `~/.config/leftwm/themes/spacecraft-software/`
2. Copy `Spacecraft_Software_wallpaper_blue.png` to the same directory.
3. Symlink as the current theme:
   ```bash
   ln -sf ~/.config/leftwm/themes/spacecraft-software ~/.config/leftwm/themes/current
   ```
4. Restart LeftWM (`Mod+Shift+R`).

**For alternative themes:**

Copy the desired theme slug's files to the theme directory in place of `steelbore`, or keep multiple theme directories and switch via symlink. Set the environment variable `SPACECRAFT_THEME=<slug>` to select a theme if your desktop environment reads it (optional per-user preference).

## Choosing a Theme

| Theme | Polarity | Best For |
|-------|----------|----------|
| `steelbore` | Dark | Default modern theme with warm tones |
| `steelbore-high-contrast` | Dark | Accessibility-focused with lifted contrast ratios |
| `steelbore-navywhite` | Light | Light canvas for bright environments |
| `solarized-light` | Light | Solarized palette reproduction (non-conforming fidelity palette) |
| `steelbore-blue` / `steelbore-magnetar` / `steelbore-biolume` | Dark | Alternative colour families |

High-contrast siblings (`-high-contrast`) offer WCAG 2.2 AA verified contrast ratios for enhanced accessibility.

**Note:** Solarized themes are fidelity palettes reproduced verbatim from their upstream source and are not adoptable as a Spacecraft Software project palette; use the Steelbore family for new projects.
