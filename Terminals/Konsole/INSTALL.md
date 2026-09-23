# Installing Spacecraft Software Themes for Konsole (KDE)

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy all `.colorscheme` files from `themes/` to `~/.local/share/konsole/`:
   ```sh
   cp themes/*.colorscheme ~/.local/share/konsole/
   ```

2. Open Konsole → **Settings** → **Edit Current Profile** → **Appearance**.

3. Select your preferred theme from the colour scheme list (e.g., "Steelbore" for the default).

4. Click **Apply**.

## Choosing a theme

| Theme | Variant | Best for | Notes |
|-------|---------|----------|-------|
| **Steelbore** | Default (modern) | Most users | WCAG AA verified, canonical Spacecraft Software palette |
| Steelbore High Contrast | Accessible | Low vision, bright environments | Higher contrast, lifted colours per §11.1.1 |
| Steelbore Blue | Alternate palette | Tonal preference | Electric blue accent, §11.3.1 |
| Steelbore Blue High Contrast | Alternate + accessible | Low vision + blue preference | Lifted variant of Steelbore Blue |
| Steelbore Magnetar | Alternate palette | Tonal preference | Energetic magenta tones, §11.3.2 |
| Steelbore Magnetar High Contrast | Alternate + accessible | Low vision + magenta preference | Lifted variant of Steelbore Magnetar |
| Steelbore Biolume | Alternate palette | Tonal preference | Neon green accent, §11.3.3 |
| Steelbore Biolume High Contrast | Alternate + accessible | Low vision + green preference | Lifted variant of Steelbore Biolume |
| Steelbore NavyWhite | Light canvas | Bright/daylight use | Light theme, navy text on white-ish canvas |
| Steelbore NavyWhite High Contrast | Light + accessible | Low vision + bright use | High-contrast light theme |
| Tokyo Night | Alternate palette | Tonal preference | Cool Tokyo night aesthetic, §11.3.5 |
| Tokyo Night High Contrast | Alternate + accessible | Low vision + cool preference | Lifted variant of Tokyo Night |
| Steelbore Hanzo Steel | Alternate palette | Tonal preference | Metallic steel tones, §11.3.6 |
| Steelbore Hanzo Steel High Contrast | Alternate + accessible | Low vision + steel preference | Lifted variant of Steelbore Hanzo Steel |
| Steelbore BlackPinkPanther | Alternate palette | Tonal preference | Bold black and pink, §11.3.7 |
| Steelbore BlackPinkPanther High Contrast | Alternate + accessible | Low vision + bold preference | Lifted variant of Steelbore BlackPinkPanther |
| Steelbore Green | Alternate palette | Tonal preference | Forest green accent, §11.3.8 |
| Steelbore Green High Contrast | Alternate + accessible | Low vision + green preference | Lifted variant of Steelbore Green |
| Steelbore Green Alt | Alternate palette | Tonal preference | Alternate green palette, §11.3.9 |
| Steelbore Green Alt High Contrast | Alternate + accessible | Low vision + alt-green preference | Lifted variant of Steelbore Green Alt |
| Steelbore Classic | Legacy palette | Compatibility | Six-role contract (§11.2), pre-v3 distribution |
| Solarized Dark | Fidelity palette | Solarized ecosystem | **NON-CONFORMING** — reproduced verbatim for compatibility, not adoptable as a project palette |
| Solarized Light | Fidelity palette | Solarized ecosystem | **NON-CONFORMING** — reproduced verbatim for compatibility, not adoptable as a project palette |

### Environment variable

On systems that support it, set `SPACECRAFT_THEME=<slug>` to auto-select a theme when Konsole starts (e.g., `export SPACECRAFT_THEME=steelbore-high-contrast`).
