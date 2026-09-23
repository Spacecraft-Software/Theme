# Spacecraft Software for Android Studio

This plugin implements the Spacecraft Software Steelbore palette family
(The Steelbore Standard §11) across the Android Studio interface —
`steelbore` (Steelbore Modern) by default, with every alternate palette and
accessibility variant selectable alongside it.

## 📁 Source structure

- `src/META-INF/plugin.xml` — plugin descriptor; one `<themeProvider>` per
  registered hex theme.
- `src/<slug>.theme.json` — UI theme overrides, one per theme.
- `src/<slug>.xml` — editor colour scheme, one per theme.
- `themes/<slug>.icls` — the same editor colour scheme, standalone, for
  **Settings → Editor → Color Scheme → Import**.

Every file here is **generated** by `tools/steelbore_themes` from
`Steelbore/steelbore.toml`; never hand-edit `src/` or `themes/` — edit the
renderer (`tools/steelbore_themes/renderers/jetbrains.py`) and regenerate.

## 🚀 Installation

1. Open **Android Studio**.
2. Go to **Settings** → **Plugins**.
3. Install from disk (`spacecraft-software-androidstudio-theme.zip`) or via
   the build instructions in `INSTALL.md`, same as IntelliJ.

See `INSTALL.md` for the full install matrix, including the `.icls`-only path
and the full theme table.

## 🎨 Palette

`steelbore` (Steelbore Modern) is the default; every reference goes through
the §11.1 role tokens, never a bare hex. Values are read from
`Steelbore/steelbore.toml` — see `INSTALL.md` for the full theme table.
