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

## Method 1: Install from VSIX (Recommended)

1. Open Antigravity.
2. Open the Command Palette (`Ctrl+Shift+P`).
3. Type **Extensions: Install from VSIX…**
4. Select `spacecraft-software-antigravity/themes-antigravity-2.0.0.vsix`.
5. Open Command Palette → **Preferences: Color Theme** → select **Steelbore**
   (or any theme from the table below).

### Verify the VSIX first (optional)

`Editors/SHA256SUMS` lists the checksum of every pre-built `.vsix` and is
signed with the maintainer's Ed25519 SSH key. From the `Editors/` directory:

```sh
ssh-keygen -Y verify -f allowed_signers -I Mohamed.Hammad@SpacecraftSoftware.org \
  -n file -s SHA256SUMS.sig < SHA256SUMS
sha256sum -c SHA256SUMS
```

Both must succeed (`Good "file" signature …`, then `OK` per file) before you
install.

## Method 2: Manual Installation

1. Copy the `spacecraft-software-antigravity/` folder to the Antigravity
   extensions directory:
   - **Windows:** `%USERPROFILE%\.antigravity\extensions\` (or equivalent)
   - **macOS/Linux:** `~/.antigravity/extensions/`
2. Restart the editor.
3. Open Command Palette → **Preferences: Color Theme** → select **Steelbore**
   (or any theme from the table below).

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
