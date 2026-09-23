# Installing Spacecraft Software Mod for Opera GX

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

This directory ships the full **Steelbore palette family** (The Steelbore
Standard §11) as 24 Opera GX mods, one manifest under
`themes/<slug>/manifest.json` (with its `themes/<slug>/license.txt`
sidecar). **Steelbore** (`steelbore`) is the default; every palette also
ships a `-high-contrast` sibling for §18.1 accessible mode.
`solarized-dark` / `solarized-light` are §11.5 **fidelity palettes** —
reproduced verbatim from upstream Solarized for interoperability,
non-conforming, and not adoptable as a project palette. Opera GX mods have
no ANSI colour concept, so there is no `steelbore-mono` variant here.

Each mod sets the browser's `gx_accent` (chrome accent) and
`gx_secondary_base` (panel/sidebar base) colours from that theme's `accent`
and `surface` roles — install only the one you want active; Opera GX
applies one mod at a time.

## Method 1: Load as Unpacked Mod (Recommended)

1. Open Opera GX.
2. Navigate to `opera://extensions`.
3. Enable **Developer mode** (toggle in the top-right corner).
4. Click **Load unpacked**.
5. Select the `themes/<slug>/` folder for the theme you want (e.g.
   `themes/steelbore/`).
6. The mod will appear in your mod list and can be activated.

## Method 2: Load from ZIP

1. Open Opera GX.
2. Navigate to `opera://extensions`.
3. Enable **Developer mode**.
4. Drag and drop `themes/spacecraft-software-opera-gx-<slug>.zip` onto the
   extensions page.

## Method 3: Upload to GX Mod Store

1. Visit [GX.store](https://store.gx.me/) to create a developer account.
2. Upload the contents of a `themes/<slug>/` folder as a new Mod.
3. Once approved, users can install it directly from the GX Mod Store.

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

## What's Included

- **Theme Colours:** every Steelbore palette family theme, as an Opera GX
  `gx_accent` / `gx_secondary_base` HSL pair.
- **License:** GPL-3.0-or-later (`themes/<slug>/license.txt` per mod,
  `license.txt` at this directory's root).

All 24 mods are generated from `tools/steelbore_themes` — see
`tools/README.md` in this repository. Do not hand-edit a file under
`themes/`; edit the renderer and regenerate.
