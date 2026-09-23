# Spacecraft Software for JetBrains IDEs

This plugin implements the Spacecraft Software Steelbore palette family
(The Steelbore Standard §11) across the entire JetBrains IDE interface —
`steelbore` (Steelbore Modern) by default, with every alternate palette and
accessibility variant selectable alongside it.

## 📁 Source structure

- `src/META-INF/plugin.xml` — plugin descriptor; one `<themeProvider>` per
  registered hex theme.
- `src/<slug>.theme.json` — UI component colour overrides, one per theme.
- `src/<slug>.xml` — editor colour scheme, one per theme.
- `themes/<slug>.icls` — the same editor colour scheme, standalone, for
  **Settings → Editor → Color Scheme → Import**.

Every file here is **generated** by `tools/steelbore_themes` from
`Steelbore/steelbore.toml`; never hand-edit `src/` or `themes/` — edit the
renderer (`tools/steelbore_themes/renderers/jetbrains.py`) and regenerate.

## 🚀 How to load / test

1. Open **IntelliJ IDEA** (or any JetBrains IDE).
2. Go to **Settings** → **Plugins**.
3. Click the ⚙️ icon and select **Install Plugin from Disk…**, pointing at
   `spacecraft-software-jetbrains-theme.zip`.
4. To test during development without a JAR:
   - Use the **IntelliJ Platform Plugin Template** or **Gradle** to build the
     plugin.
   - Alternatively, point the IDE at the `src` directory if configured as a
     DevKit project.

See `INSTALL.md` for the full install matrix, including the `.icls`-only path.

## 🎨 Palette

`steelbore` (Steelbore Modern) is the default; every reference goes through
the §11.1 role tokens (`background`, `surface`, `surface-alt`, `foreground`,
`accent`, `structure`, `success`, `error`, `warning`, `focus`, `border`),
never a bare hex. Ten alternates and two non-conforming Solarized fidelity
themes ship alongside it. Values are read from `Steelbore/steelbore.toml` (a
verbatim copy of the `steelbore-color-palette` skill's contract) — see
`INSTALL.md` for the full theme table, and never retype a hex here.
