# Installing Spacecraft Software Themes for MangoWC

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

The Spacecraft Software theme distribution for MangoWC ships 24 palette-conforming themes plus 2 Solarized fidelity variants, generated from the canonical palette family defined in The Steelbore Standard §11.

1. **Copy theme files** from `themes/` to your MangoWC config directory:
   ```bash
   cp themes/*.toml ~/.config/mangowc/
   ```

2. **Set the theme** in your MangoWC config file (`~/.config/mangowc/mangowc.toml`):
   ```toml
   theme = "steelbore"  # or any other theme slug
   ```

3. **Optional:** Copy the included wallpaper to your wallpapers directory:
   ```bash
   cp Spacecraft_Software_wallpaper_blue.png ~/Pictures/wallpapers/
   ```

4. **Restart MangoWC** or reload the config (`SPACECRAFT_THEME=<slug> mangowc`).

## Available Themes

| Theme Slug | Display Name | Variant | Palette Conformance |
|---|---|---|---|
| `steelbore` | Steelbore | **Default (Modern)** | WCAG 2.2 AA |
| `steelbore-high-contrast` | Steelbore High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-blue` | Steelbore Blue | Alternate palette | WCAG 2.2 AA |
| `steelbore-blue-high-contrast` | Steelbore Blue High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-magnetar` | Steelbore Magnetar | Alternate palette | WCAG 2.2 AA |
| `steelbore-magnetar-high-contrast` | Steelbore Magnetar High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-biolume` | Steelbore Biolume | Alternate palette | WCAG 2.2 AA |
| `steelbore-biolume-high-contrast` | Steelbore Biolume High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-navywhite` | Steelbore NavyWhite | **Light canvas** | WCAG 2.2 AA |
| `steelbore-navywhite-high-contrast` | Steelbore NavyWhite High Contrast | Light + accessible | WCAG 2.2 AAA |
| `tokyonight` | Tokyo Night | Alternate palette | WCAG 2.2 AA |
| `tokyonight-high-contrast` | Tokyo Night High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-hanzosteel` | Steelbore Hanzo Steel | Alternate palette | WCAG 2.2 AA |
| `steelbore-hanzosteel-high-contrast` | Steelbore Hanzo Steel High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-blackpinkpanther` | Steelbore BlackPinkPanther | Alternate palette | WCAG 2.2 AA |
| `steelbore-blackpinkpanther-high-contrast` | Steelbore BlackPinkPanther High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-green` | Steelbore Green | Alternate palette | WCAG 2.2 AA |
| `steelbore-green-high-contrast` | Steelbore Green High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-greenalt` | Steelbore Green Alt | Alternate palette | WCAG 2.2 AA |
| `steelbore-greenalt-high-contrast` | Steelbore Green Alt High Contrast | Accessible sibling | WCAG 2.2 AAA |
| `steelbore-classic` | Steelbore Classic | Legacy six-role contract | WCAG 2.2 AA |
| `steelbore-classic-high-contrast` | Steelbore Classic High Contrast | Legacy + accessible | WCAG 2.2 AAA |
| `solarized-dark` | Solarized Dark | **Fidelity palette** (non-conforming) | Not verified |
| `solarized-light` | Solarized Light | **Fidelity palette** (non-conforming) | Not verified |

**Note:** The Solarized themes (`solarized-dark`, `solarized-light`) are fidelity palettes reproduced verbatim from upstream and do not adopt the Spacecraft Software palette contract. They are provided for compatibility but should not be adopted as a project palette.

## Theme Format

Each theme is a standalone TOML file containing:
- `[Theme]`: theme metadata (`name`)
- `[Colors]`: colour assignments (`bg_color`, `fg_color`, `active_border`, `inactive_border`, `button_bg`, `button_fg`)
- `[Window]`: window settings (`border_width`, `border_radius`)
- `[Gaps]`: gap settings (`inner`, `outer`)

Themes are generated from the canonical palette family (The Steelbore Standard §11). Do not edit them by hand — regenerate from source if a change is needed.
