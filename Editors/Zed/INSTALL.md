# Installing Spacecraft Software Theme for Zed Editor

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Zed theme-family file per registered theme of the
Steelbore palette family (The Steelbore Standard §11). Each file has exactly
one theme entry, named for that theme. `steelbore.json` is the default; every
conforming palette also ships a `-high-contrast` sibling for accessible mode.
`steelbore.json` at the repo root of this directory (also bundled as
`steelbore.json` inside the archive) is a single family named **Steelbore**
holding every theme, default first — install that one file for the whole set
at once. All files are generated from `Steelbore/steelbore.toml` — do not
edit them.

## Installation

### Whole family (recommended)

1. Copy `steelbore.json` to your Zed themes directory:
   - **macOS/Linux:** `~/.config/zed/themes/`
   - **Windows:** `%APPDATA%\Zed\themes\`
2. Open Zed → **Command Palette** (`Ctrl+Shift+P`) → **theme selector: toggle**.
3. Pick any Steelbore theme from the list — they are all installed together.

### One theme only

1. Copy the file for the theme you want from `themes/` (for example
   `themes/steelbore-navywhite.json`) into the same Zed themes directory.
2. Select it from the theme selector as above.

### Settings file

Add to your Zed `settings.json`:
```json
{
    "theme": "Steelbore"
}
```
Use the theme's own `name` (see the table below) to pick a specific member,
e.g. `"Steelbore High Contrast"` or `"Steelbore NavyWhite"`.

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.json` | Steelbore Modern | **default** |
| `steelbore-high-contrast.json` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.json`, `steelbore-magnetar.json`, `steelbore-biolume.json`, `tokyonight.json`, `steelbore-hanzosteel.json`, `steelbore-blackpinkpanther.json`, `steelbore-green.json`, `steelbore-greenalt.json` | alternates (§11.3) | each with a `-high-contrast.json` sibling |
| `steelbore-navywhite.json` | Steelbore NavyWhite | the family's light canvas (`"appearance": "light"`) |
| `steelbore-classic.json` | Steelbore Classic | the original six-role look (§11.2) |
| `solarized-dark.json`, `solarized-light.json` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |

Zed's theme schema is hex-only, so it cannot express the palette-independent
`steelbore-mono` theme; for `NO_COLOR` sessions leave Zed on its own defaults.
