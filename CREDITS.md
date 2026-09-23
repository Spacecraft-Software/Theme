<!--
SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# CREDITS

Third-party work this repository substantially builds on (The Steelbore Standard
§15.3). SPDX metadata in `REUSE.toml` covers the mechanical license obligations;
this file is the human-readable record.

| Name | Author(s) | License | Source | Scope |
|------|-----------|---------|--------|-------|
| Tokyo Night | enkia | MIT | <https://github.com/enkia/tokyo-night-vscode-theme> | The `tokyonight` palette in `Steelbore/steelbore.toml` reproduces the Night variant's colour values verbatim and registers them as a conforming alternate (§11.3.5). |
| Solarized | Ethan Schoonover | MIT | <https://ethanschoonover.com/solarized> | The `solarized-dark` and `solarized-light` fidelity palettes (§11.5) reproduce the sixteen Solarized values exactly, unmodified, for interoperability. |
| Catppuccin Powerline preset for Starship | Catppuccin contributors; Starship contributors | MIT | <https://starship.rs/presets/catppuccin-powerline> | `Shells/Starship/themes/*.toml` keep the preset's format string and module configuration verbatim and substitute only the named palette table with Steelbore role tokens. |
| Steelbore palette family | Mohamed Hammad & Spacecraft Software | GPL-3.0-or-later | <https://Construct.SpacecraftSoftware.org/> (`steelbore-color-palette` skill) | `Steelbore/steelbore.toml` is a verbatim copy of the skill's `assets/steelbore.toml`; the skill is the canonical source. |
