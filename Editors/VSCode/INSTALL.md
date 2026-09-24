# Installing Spacecraft Software Theme for Visual Studio Code

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

This package ships the full **Steelbore palette family** (The Steelbore
Standard §11) as 24 VS Code colour themes, one JSON file per theme under
`spacecraft-software-theme/themes/<slug>.json`. **Steelbore** (`steelbore`)
is the default; every palette also ships a `-high-contrast` sibling for
§18.1 accessible mode. `solarized-dark` / `solarized-light` are §11.5
**fidelity palettes** — reproduced verbatim from upstream Solarized for
interoperability, non-conforming, and not adoptable as a project palette.

## Method 1: The installer script (Recommended)

`Editors/install-extensions.sh` (POSIX sh) and its Nushell twin
`Editors/install-extensions.nu` install the extension into every VS Code,
VSCodium and Antigravity they detect, native or Flatpak, after verifying the
signed checksums below. From the `Editors/` directory:

```sh
./install-extensions.sh --dry-run          # show the plan
./install-extensions.sh                    # install from the VSIX files here
./install-extensions.sh --source release   # from the latest GitHub release
./install-extensions.sh --source marketplace --editor code
```

`nu install-extensions.nu` takes the same flags. `--help` lists them all.

## Method 2: Install from VSIX

1. Open VS Code.
2. Open the Command Palette (`Ctrl+Shift+P`).
3. Type **Extensions: Install from VSIX…**
4. Select `spacecraft-software-theme/themes-2.0.0.vsix`.
5. Restart VS Code when prompted.
6. Open Command Palette → **Preferences: Color Theme** → select **Steelbore**
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

## Method 3: Without the VS Code CLI

Copying the folder into the extensions directory is **not enough**: once the
directory holds an `extensions.json` (it does after any normal install), VS
Code ignores every folder that file does not list. The installer's `unpack`
method extracts the VSIX and adds the entry for you:

```sh
./install-extensions.sh --editor code --method unpack
```

Extensions directories: `~/.vscode/extensions` (native),
`~/.var/app/com.visualstudio.code/data/vscode/extensions` (Flatpak),
`%USERPROFILE%\.vscode\extensions` (Windows). Restart VS Code afterwards.

## Method 4: Package and Publish

1. Install `vsce`: `npm install -g @vscode/vsce`
2. Run `vsce package` inside the `spacecraft-software-theme/` folder.
3. Upload the `.vsix` to the [VS Code Marketplace](https://marketplace.visualstudio.com/).

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
