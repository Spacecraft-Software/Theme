# Installing Spacecraft Software Theme for Visual Studio

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

Supports: Visual Studio 2022 (Community, Professional, Enterprise).

This package ships the full **Steelbore palette family** (The Steelbore
Standard §11) as 24 Visual Studio colour themes, one `.vstheme` file per
theme under `themes/<slug>.vstheme`. **Steelbore** (`steelbore`) is the
default; every palette also ships a `-high-contrast` sibling for §18.1
accessible mode. `solarized-dark` / `solarized-light` are §11.5 **fidelity
palettes** — reproduced verbatim from upstream Solarized for
interoperability, non-conforming, and not adoptable as a project palette.

## Method 1: Install from VSIX (Recommended)

1. Double-click the `spacecraft-software-visualstudio.vsix` file.
2. The Visual Studio Installer will launch and install every theme in the
   table below.
3. Restart Visual Studio.
4. Go to **Tools** → **Options** → **Environment** → **General** →
   **Color theme** → select **Steelbore** (or any theme from the table
   below).

## Method 2: Install via Extensions Menu

1. Open Visual Studio.
2. Go to **Extensions** → **Manage Extensions**.
3. Click **⚙️** or use **Install from file** and select the `.vsix` file.
4. Restart Visual Studio.

## Method 3: Manual import of one theme

1. Open **Tools** → **Options** → **Environment** → **General**.
2. Use **Import and Export Settings** (or the Color Theme Designer
   extension) to import a single file from `themes/<slug>.vstheme`.

## Method 4: Publish to VS Marketplace

1. Package the theme using the [VSIX packaging tool](https://learn.microsoft.com/en-us/visualstudio/extensibility/).
2. Upload `spacecraft-software-visualstudio.vsix` to the
   [Visual Studio Marketplace](https://marketplace.visualstudio.com/).

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
