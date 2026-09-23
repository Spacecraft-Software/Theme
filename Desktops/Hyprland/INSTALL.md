# Installing Spacecraft Software Themes for Hyprland

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

Copy `themes/` to your Hyprland configuration directory and source a theme file:

```bash
mkdir -p ~/.config/hypr/themes
cp themes/* ~/.config/hypr/themes/
```

Then in `~/.config/hypr/hyprland.conf`, source your chosen theme:

```ini
source = ~/.config/hypr/themes/steelbore.conf
```

## Choosing a theme

| Theme | Canvas | Type | Status |
|-------|--------|------|--------|
| **steelbore** | Dark | Default | WCAG 2.2 AA verified |
| steelbore-high-contrast | Dark | Accessible sibling | Enhanced contrast |
| steelbore-blue, -high-contrast | Dark | Alternate | Blue-shifted palette |
| steelbore-magnetar, -high-contrast | Dark | Alternate | High-energy theme |
| steelbore-biolume, -high-contrast | Dark | Alternate | Bioluminescent palette |
| steelbore-navywhite, -high-contrast | Light | Alternate | Light canvas, dark text |
| tokyonight, -high-contrast | Dark | Alternate | Tokyo Night inspired |
| steelbore-hanzosteel, -high-contrast | Dark | Alternate | Hanzo Steel theme |
| steelbore-blackpinkpanther, -high-contrast | Dark | Alternate | High-energy black/pink |
| steelbore-green, -high-contrast | Dark | Alternate | Green-focused palette |
| steelbore-greenalt, -high-contrast | Dark | Alternate | Green variant |
| steelbore-classic | Dark | Legacy | Six-role contract (§11.2) |
| solarized-dark, solarized-light | — | Fidelity | **Non-conforming** (§11.5) — not adoptable as project palette |

**Default:** `steelbore` (dark, modern, verified against Void Navy).  
**High-contrast siblings** of each palette theme offer enhanced visibility for accessibility; they carry the `-high-contrast` suffix and use lifted role colours (§11.1.1).  
**Solarized themes** reproduce the Solarized palette verbatim per §11.5 but do not conform to the Spacecraft Software colour contract and are not adoptable as a project theme.

## Per-system default

Set the environment variable to change the default on login:

```bash
export SPACECRAFT_THEME=steelbore-navywhite
```

Hyprland does not read this variable; it is provided for multi-system consistency and shell integration.

## Manual customization

The theme file sets colours only. Layout settings (gaps, borders, blur, shadows) are preserved from the legacy configuration. To customize them, edit `~/.config/hypr/hyprland.conf` directly.
