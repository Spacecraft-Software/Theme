# Installing Spacecraft Software Theme for Niri

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

Each theme is a standalone KDL configuration file under `themes/`. To use a theme:

1. Choose a theme file from the `themes/` directory (default: `steelbore.kdl`)
2. Include it in your Niri configuration:
   ```kdl
   include "themes/steelbore.kdl"
   ```
   Replace `steelbore` with your chosen theme slug.
3. Copy the wallpaper assets to your wallpapers directory if desired.
4. Reload your Niri configuration.

## Available Themes

The **Steelbore** palette family (v3.5.0, The Steelbore Standard §11.1) includes 24 hex colour themes, all rendered to native Niri KDL configuration blocks:

| Slug | Name | Variant |
|------|------|---------|
| `steelbore` ⭐ | Steelbore | default |
| `steelbore-high-contrast` | Steelbore High Contrast | accessible |
| `steelbore-blue`, `-high-contrast` | Steelbore Blue | alternate |
| `steelbore-magnetar`, `-high-contrast` | Steelbore Magnetar | alternate |
| `steelbore-biolume`, `-high-contrast` | Steelbore Biolume | alternate |
| `steelbore-navywhite`, `-high-contrast` | Steelbore NavyWhite | light canvas |
| `tokyonight`, `-high-contrast` | Tokyo Night | alternate |
| `steelbore-hanzosteel`, `-high-contrast` | Steelbore Hanzo Steel | alternate |
| `steelbore-blackpinkpanther`, `-high-contrast` | Steelbore BlackPinkPanther | alternate |
| `steelbore-green`, `-high-contrast` | Steelbore Green | alternate |
| `steelbore-greenalt`, `-high-contrast` | Steelbore Green Alt | alternate |
| `steelbore-classic`, `-high-contrast` | Steelbore Classic | legacy six-role |
| `solarized-dark`, `solarized-light` | Solarized | fidelity (non-conforming) |

**⭐ Steelbore** is the default and recommended theme. Each theme has a `-high-contrast` sibling for accessibility; both conform to WCAG 2.2 AA contrast ratios.

**Solarized** is a fidelity reproduction of the Solarized palette (not adoptable as a project palette per §11.5).

## Environment Variable

You may also set the `SPACECRAFT_THEME` environment variable and parse it in your Niri configuration:

```kdl
include "themes/${env.SPACECRAFT_THEME:steelbore}.kdl"
```

This allows dynamic theme selection per shell session.

## Customisation

Each theme file is a standard KDL configuration block that sets:

- **focus-ring**: Window focus indicator with active-gradient (accent to focus) and inactive-color (surface)
- **border**: Window borders with active-color (structure) and inactive-color (background)
- **opacity**: Terminal window transparency for wallpaper visibility

Edit any theme file to adjust gaps, border widths, gradients, or opacity settings to your preference.
