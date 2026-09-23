# Spacecraft Software Theme for Visual Studio (IDE)

Bring the full **Steelbore palette family** (The Steelbore Standard §11) to
Visual Studio 2022 — 24 colour themes, one `.vstheme` file per theme under
`themes/<slug>.vstheme`. **Steelbore** (`steelbore`) is the default; every
palette also ships a `-high-contrast` sibling for §18.1 accessible mode.
`solarized-dark` / `solarized-light` are §11.5 **fidelity palettes** —
reproduced verbatim from upstream Solarized for interoperability,
non-conforming, and not adoptable as a project palette.

See `INSTALL.md` for the full install methods; the short version:

## Installation

### From VSIX (recommended)
1. Double-click `spacecraft-software-visualstudio.vsix`, or install it from
   **Extensions → Manage Extensions → Install from file**.
2. Restart Visual Studio.
3. **Tools → Options → Environment → General → Color theme** → select
   **Steelbore** (or any theme — see `INSTALL.md` for the full table).

### Manual import of one theme
1. Open **Tools → Options → Environment → General**.
2. Import a single file from `themes/<slug>.vstheme` with **Import and
   Export Settings** (or the Color Theme Designer extension).

### Packaging (VSIX)
To rebuild the distributable `.vsix`:
1. Run `python3 -m steelbore_themes package --target visualstudio` from
   `tools/` in this repository (regenerates `extension.vsixmanifest`,
   `[Content_Types].xml` and both archives from `themes/`).

## Palette

Every colour in every theme comes from the canonical Steelbore palette
family — see the `steelbore-color-palette` skill / `Steelbore/steelbore.toml`
for the full role and hex contract; this file does not restate hex values
that drift with the palette. `INSTALL.md` has the complete theme table.

## License

Copyright (C) 2026 Mohamed Hammad. Distributed under the GNU General Public
License v3.0-or-later.

---
*Part of the Spacecraft Software Ecosystem.*
