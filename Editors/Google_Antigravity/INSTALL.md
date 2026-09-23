# Installing Spacecraft Software Theme for Google Antigravity

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

This package ships the full **Steelbore palette family** (The Steelbore
Standard §11) as 24 VS Code-compatible colour themes, one JSON file per
theme under `spacecraft-software-antigravity/themes/<slug>.json`.
**Steelbore** (`steelbore`) is the default; every palette also ships a
`-high-contrast` sibling for §18.1 accessible mode. `solarized-dark` /
`solarized-light` are §11.5 **fidelity palettes** — reproduced verbatim
from upstream Solarized for interoperability, non-conforming, and not
adoptable as a project palette.

## Method 1: Manual Installation

1. Copy the `spacecraft-software-antigravity/` folder to the Antigravity
   extensions directory:
   - **Windows:** `%USERPROFILE%\.antigravity\extensions\` (or equivalent)
   - **macOS/Linux:** `~/.antigravity/extensions/`
2. Restart the editor.
3. Open Command Palette → **Preferences: Color Theme** → select **Steelbore**
   (or any theme from the table below).

## Method 2: Build a VSIX

Antigravity does not ship a pre-built `.vsix` for this package; build one
if your installation needs it:

1. Install `vsce`: `npm install -g @vscode/vsce`
2. Run `vsce package` inside the `spacecraft-software-antigravity/` folder.
3. Install the resulting `.vsix` via **Extensions: Install from VSIX…**.

## Choosing a theme

| Slug | Name | Canvas |
| --- | --- | --- |
| `steelbore` | Steelbore (**default**) | dark |
| `steelbore-high-contrast` | Steelbore High Contrast | dark |
| `steelbore-blue` / `-high-contrast` | Steelbore Blue | dark |
| `steelbore-magnetar` / `-high-contrast` | Steelbore Magnetar | dark |
| `steelbore-biolume` / `-high-contrast` | Steelbore Biolume | dark |
| `steelbore-navywhite` / `-high-contrast` | Steelbore NavyWhite | light |
| `tokyonight` / `-high-contrast` | Tokyo Night | dark |
| `steelbore-hanzosteel` / `-high-contrast` | Steelbore Hanzo Steel | dark |
| `steelbore-blackpinkpanther` / `-high-contrast` | Steelbore BlackPinkPanther | dark |
| `steelbore-green` / `-high-contrast` | Steelbore Green | dark |
| `steelbore-greenalt` / `-high-contrast` | Steelbore Green Alt | dark |
| `steelbore-classic` / `-high-contrast` | Steelbore Classic (legacy six-role) | dark |
| `solarized-dark` / `solarized-light` | Solarized (**fidelity, non-conforming**) | dark / light |

All 24 themes are generated from `tools/steelbore_themes` — see
`tools/README.md` in this repository. Do not hand-edit a file under
`themes/`; edit the renderer and regenerate.
