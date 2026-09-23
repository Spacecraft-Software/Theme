# Installing Spacecraft Software Themes for XFCE Terminal

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy all `.theme` files from the `themes/` directory to your XFCE Terminal colour schemes directory:
   - User: `~/.local/share/xfce4/terminal/colorschemes/`
   - System-wide: `/usr/share/xfce4/terminal/colorschemes/`

2. Open XFCE Terminal → **Edit** → **Preferences** → **Colors**.

3. Under **Presets**, select any available theme from the list.

## Available Themes

The bundle includes 24 colour schemes organized by palette variant. **Steelbore** is the recommended default.

| Palette | Base Theme | High-Contrast Variant | Polarity |
|---------|------------|----------------------|----------|
| Steelbore (default) | Steelbore | Steelbore High Contrast | Dark |
| Steelbore Blue | Steelbore Blue | Steelbore Blue High Contrast | Dark |
| Steelbore Magnetar | Steelbore Magnetar | Steelbore Magnetar High Contrast | Dark |
| Steelbore Biolume | Steelbore Biolume | Steelbore Biolume High Contrast | Dark |
| Steelbore NavyWhite | Steelbore NavyWhite | Steelbore NavyWhite High Contrast | Light |
| Tokyo Night | Tokyo Night | Tokyo Night High Contrast | Dark |
| Steelbore Hanzo Steel | Steelbore Hanzo Steel | Steelbore Hanzo Steel High Contrast | Dark |
| Steelbore BlackPinkPanther | Steelbore BlackPinkPanther | Steelbore BlackPinkPanther High Contrast | Dark |
| Steelbore Green | Steelbore Green | Steelbore Green High Contrast | Dark |
| Steelbore Green Alt | Steelbore Green Alt | Steelbore Green Alt High Contrast | Dark |
| Steelbore Classic | Steelbore Classic | — | Dark |
| Solarized Dark | Solarized Dark | — | Dark* |
| Solarized Light | Solarized Light | — | Light* |

\* **Solarized is a non-conforming fidelity palette** (§11.5). It is included for compatibility but does not conform to the Spacecraft Software Standard. For new projects, prefer a Steelbore palette.

## Environment Variable

Some shell environments and terminal multiplexers read `$SPACECRAFT_THEME` to automatically select a theme. Set it in your shell RC file:

```sh
export SPACECRAFT_THEME=steelbore
```
