# Installing Spacecraft Software Theme for Wave Terminal

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy one or more theme files from `themes/` to your Wave Terminal themes directory:
   - **Linux/macOS:** `~/.waveterm/themes/`
   - **Windows:** `%USERPROFILE%\.waveterm\themes\`
2. Open Wave Terminal → **Settings** → **Themes** → select your preferred theme.

## Included Themes

| Theme | Variant | Canvas | Notes |
|-------|---------|--------|-------|
| Steelbore | Default (Modern) | Dark | Recommended default; WCAG 2.2 AA verified |
| Steelbore High Contrast | Accessible mode | Dark | Enhanced contrast for accessibility (§11.1.1) |
| Steelbore Blue | Alternate modern | Dark | Cool blue palette variant |
| Steelbore Blue High Contrast | Accessible mode | Dark | Accessible variant of Steelbore Blue |
| Steelbore Magnetar | Alternate modern | Dark | Bold magnetar-inspired palette |
| Steelbore Magnetar High Contrast | Accessible mode | Dark | Accessible variant of Steelbore Magnetar |
| Steelbore Biolume | Alternate modern | Dark | Bioluminescent-inspired palette |
| Steelbore Biolume High Contrast | Accessible mode | Dark | Accessible variant of Steelbore Biolume |
| Steelbore NavyWhite | Light canvas | Light | Spacecraft Software on light background |
| Steelbore NavyWhite High Contrast | Light + accessible | Light | Accessible variant for light background |
| Steelbore Classic | Legacy | Dark | Classic six-role palette (§11.2) |
| Steelbore Classic High Contrast | Legacy + accessible | Dark | Accessible variant of Classic |
| Tokyo Night | Alternate modern | Dark | Tokyo Night-inspired variant |
| Tokyo Night High Contrast | Accessible mode | Dark | Accessible variant of Tokyo Night |
| Steelbore Hanzo Steel | Alternate modern | Dark | Steel-inspired palette variant |
| Steelbore Hanzo Steel High Contrast | Accessible mode | Dark | Accessible variant of Steelbore Hanzo Steel |
| Steelbore BlackPinkPanther | Alternate modern | Dark | Dramatic black and pink variant |
| Steelbore BlackPinkPanther High Contrast | Accessible mode | Dark | Accessible variant of Steelbore BlackPinkPanther |
| Steelbore Green | Alternate modern | Dark | Green-tinted palette variant |
| Steelbore Green High Contrast | Accessible mode | Dark | Accessible variant of Steelbore Green |
| Steelbore Green Alt | Alternate modern | Dark | Alternative green palette |
| Steelbore Green Alt High Contrast | Accessible mode | Dark | Accessible variant of Steelbore Green Alt |
| Solarized Dark | Fidelity palette | Dark | Solarized Dark (non-conforming, §11.5) |
| Solarized Light | Fidelity palette | Light | Solarized Light (non-conforming, §11.5) |

**Note:** Solarized themes are fidelity palettes reproduced verbatim and are not adoptable as project palettes. High Contrast variants (§11.1.1) are accessible-mode siblings for users requiring enhanced color separation and contrast ratios.

## Environment Variable

On systems where your shell or a launcher exports it, `SPACECRAFT_THEME=<slug>` can be used to select which theme file to install/copy — Wave itself has no native reader for it, so the manual **Settings → Themes** step above still applies:
```bash
export SPACECRAFT_THEME=steelbore-high-contrast
```
