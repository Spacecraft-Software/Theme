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

## Method 1: The installer script (Recommended)

`Editors/install-extensions.sh` (POSIX sh) and its Nushell twin
`Editors/install-extensions.nu` install the extension into Antigravity
(`antigravity`) and Antigravity IDE (`antigravity-ide`), and into any VS Code
or VSCodium they find, after verifying the signed checksums below. From the
`Editors/` directory:

```sh
./install-extensions.sh --dry-run                  # show the plan
./install-extensions.sh --editor antigravity-ide   # install from the VSIX here
./install-extensions.sh --source release           # from the latest GitHub release
```

On NixOS, the FHS-wrapped Antigravity commands open the editor instead of
installing, so the installer switches those editors to its `unpack` method
automatically. `nu install-extensions.nu` takes the same flags.

## Method 2: Install from VSIX

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

## Method 3: Without the editor's CLI

Copying the folder into the extensions directory is **not enough**: once the
directory holds an `extensions.json` (it does after any normal install), the
editor ignores every folder that file does not list. The installer's `unpack`
method extracts the VSIX and adds the entry for you:

```sh
./install-extensions.sh --editor antigravity-ide --method unpack
```

Extensions directories: `~/.antigravity/extensions` (Antigravity) and
`~/.antigravity-ide/extensions` (Antigravity IDE); on Windows the same names
under `%USERPROFILE%`. Restart the editor afterwards.

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
