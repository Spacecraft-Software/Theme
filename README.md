# Spacecraft Software Theme

The Spacecraft Software visual identity — the **Steelbore palette family** of
The Steelbore Standard §11 — rendered for every editor, terminal, desktop,
shell, browser and CLI in the maintainer's toolchain.

Every theme file here is **generated** from one source, `Steelbore/steelbore.toml`
(palette family v3.5.0, Standard v2.08), by `tools/steelbore_themes`. Each
platform folder ships one file per theme under `themes/<slug>.<ext>`:

| Slug | Palette | Notes |
|------|---------|-------|
| `steelbore` | Steelbore Modern | **default** — Void Navy canvas, Plasma Orange accent |
| `steelbore-blue` · `steelbore-magnetar` · `steelbore-biolume` · `steelbore-navywhite` (light) · `tokyonight` · `steelbore-hanzosteel` · `steelbore-blackpinkpanther` · `steelbore-green` · `steelbore-greenalt` | nine alternates (§11.3) | opt-in |
| `<slug>-high-contrast` | accessible-mode sibling of each palette above | every token ≥ 7:1 on the canvas (§11.1.1) |
| `steelbore-classic` (+ `-high-contrast`) | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark` · `solarized-light` | Solarized, verbatim | fidelity palettes (§11.5): **not WCAG-conforming**, shipped for interoperability |
| `steelbore-mono` | 4-bit ANSI names | `NO_COLOR` theme; shells, Starship and the TTY only |

Pick a theme by slug; set `SPACECRAFT_THEME=<slug>` where a platform's
installer reads it (§11.6). Each folder's `INSTALL.md` has the details.

## Project Posture

Spacecraft Software is a **personal hobby project**. This repository is
developed at hobby pace and shaped around the maintainer's own use case, not a
general audience.

- **No warranty, no liability.** See [`NOTICE.md`](./NOTICE.md).
- **Contributions are welcome but not guaranteed.** See [`CONTRIBUTING.md`](./CONTRIBUTING.md).
- **Forking is encouraged.** GPL-3.0-or-later is there for exactly that.
- **Security reports:** see [`SECURITY.md`](./SECURITY.md).

Assurance category **D** (§19): a static configuration distribution with no
runtime; conformance to The Steelbore Standard v2.08 is claimed in full for the
generated artifacts and tailored for the repository (no Texinfo manual, no
packaging manifests — nothing here is installed by a package manager).

## Supported environments

### Editors (`Editors/`)
VS Code and Google Antigravity (one extension, all themes), Zed (family file
plus per-theme files), Lapce, JetBrains IDEs and Android Studio (one plugin,
all themes, plus importable `.icls` schemes), Visual Studio 2022 (`.vsix`),
Azure DevOps.

### Terminals (`Terminals/`)
Alacritty, Ghostty, GNOME Terminal (dconf profile scripts), iTerm2, Kitty,
Konsole, Rio, Warp, Wave, WezTerm, Windows Terminal (`schemes.json` for one
paste), XFCE Terminal.

### Desktops and window managers (`Desktops/`)
GNOME (libadwaita GTK 4 + Shell CSS), KDE Plasma (`.colors`), COSMIC (`.ron`),
XFCE and MATE (GTK CSS + Metacity), Hyprland, Niri, LeftWM (+ Polybar),
MangoWC, Windows (`.theme` + console and accent `.reg`).

### Shells (`Shells/`)
Bash, Zsh, Fish, Csh/Tcsh, Ion, Nushell prompt and syntax modules, a Starship
Powerline preset, and Linux TTY palette scripts. These also ship `steelbore-mono`.

### Browsers (`Browsers/`)
Chromium family (Chrome, Edge, Brave, Trivalent, Arc, Opera One) as MV3 theme
extensions, Gecko family (Firefox, Zen, Tor Browser) as MV2 theme `.xpi`, Opera
GX as a GX mod. One theme per extension archive.

### CLIs, bootloaders, AI (`CLIs/`, `Bootloaders/`, `AI/`)
Claude Code status-line fragments, the Zamak bootloader theme, and the three
Claude skills this repository depends on (`spacecraft-theme-factory`,
`spacecraft-brand-guidelines`, `steelbore-color-palette`) as `.skill` bundles.

## Installation

Every platform folder contains an `INSTALL.md` and, where the platform consumes
one, a pre-built archive (`.zip`, `.tar.gz`, `.xpi`, `.vsix`). Copy the theme
file(s) for the slug you want and follow the folder's instructions.

For VS Code, VSCodium, Antigravity and Antigravity IDE, native or Flatpak,
`Editors/install-extensions.sh` (POSIX sh) or `Editors/install-extensions.nu`
(Nushell) installs the extension into every editor it detects. It installs
from the VSIX files in this tree, a GitHub release, or the VS Code Marketplace
and Open VSX, and checks the signed `Editors/SHA256SUMS` first. Run it with
`--help`.

The all-in-one installer (`Scripts/install-spacecraft-software.sh`) and the
Microsoft Office VBA macro referenced by earlier versions of this README are
**not yet in the tree** — they remain on the backlog.

## Regenerating

```sh
cd tools
python3 -m steelbore_themes generate    # every target
python3 -m steelbore_themes validate    # exit 1 on any drift or palette violation
python3 -m steelbore_themes package     # rebuild the archives
```

Plain Python ≥ 3.11, no dependencies. See `tools/README.md` for the renderer
contract and `AGENTS.md` for the repository invariants.

## Typography (§12)

Share Tech Mono for headings, Inconsolata for body and code, system
`monospace` as fallback — all OFL. No proprietary fonts anywhere.

## Maintainer

Mohamed Hammad — <Mohamed.Hammad@SpacecraftSoftware.org>
<https://Theme.SpacecraftSoftware.org/>

**Copyright (C) 2026 Mohamed Hammad & Spacecraft Software** · software `GPL-3.0-or-later`, documentation `CC-BY-SA-4.0`
