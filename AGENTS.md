# AGENTS.md

## What this repo is

A multi-platform theme distribution for the Spacecraft Software brand — static configuration assets (no application code, no build system, no test suite). Each top-level directory targets a category of host environment and ships the theme in that platform's native format (JSON for VSCode/Zed, XML+`.theme.json` for JetBrains, `.colors` for KDE, `.ron` for COSMIC, GTK CSS for GNOME/XFCE/MATE, TOML for Lapce/Starship/Zamak, KDL for Niri, `.conf` for Hyprland, manifest+CSS for browser extensions, `.reg`/`.theme`/`.themepack` for Windows, ANSI color scripts for shells/terminals, etc.).

Most platform folders contain **both** an unpacked source tree **and** a pre-built archive (`.zip` / `.tar.gz` / `.xpi` / `.vsix`). When editing, modify the unpacked source — the archives are deliverables and need to be re-zipped from the source folder when changes are ready to ship.

**Aspirational README references** — `README.md` documents several artifacts that don't yet exist in the tree. Don't try to invoke or locate them; treat them as a backlog:
- `Scripts/install-spacecraft-software.sh` (and the whole `Scripts/` directory)
- Per-shell installers it sources (`install-tty-colors.sh`, `spacecraft-software.sh`, `spacecraft-software.nu`, `spacecraft-software.ion`)
- The Microsoft Office VBA macro (`Spacecraft-Software-Office-Theme.bas`) — there is no `Office/` category folder either

`Themes.md` at the repo root is a two-line pointer to the published VSCode / Antigravity marketplace listings. Note those URLs still use the pre-rename `SteelBore` publisher namespace — fix when the listings are re-published under `Spacecraft-Software`.

## Repo identity and sync

- **Canonical remote**: `git@github.com:Spacecraft-Software/Theme.git` (public, default branch `main`).
- **Sync model**: this working tree is a clone. Edits become canonical only after `git push origin main`. There is no CI or release automation yet.
- **History**: an older copy of this tree lived as a `Theme/` subfolder inside `UnbreakableMJ/Steelbore` (Mohamed's *personal* monorepo, name unchanged per the brand rename's UnbreakableMJ exception). That subfolder has been retired (PR `UnbreakableMJ/Steelbore#1`, merged 2026-05-13) and replaced with a redirect README pointing here. If you spot stale references to the monorepo path anywhere, fix them to point to `github.com/Spacecraft-Software/Theme`.
- **Local-only files** (already in `.gitignore`, do not stage): `Chat.txt`, `.claude/settings.local.json`. `AGENTS.md` and `CLAUDE.md` are **tracked** as of Standard §5.7 — commit them like any other file.
- **Governance docs**: `CONTRIBUTING.md` (engineering/UX rules — see below) and `SECURITY.md` (vulnerability reporting) are the authoritative project policies.
- **Line endings**: all text files are LF. `.gitattributes` declares `* text=auto eol=lf` — Git will renormalize on commit, so don't fight it with editor settings that re-introduce CRLF.

## The canonical palette

Every theme target must render the same brand identity. The authoritative source is the `css` file at the repo root (it is a file, not a directory, despite the name):

| Token                | Hex       | Role                          |
| -------------------- | --------- | ----------------------------- |
| `--scs-void-navy`    | `#000027` | Primary background            |
| (lighter navy)       | `#050530` | Secondary background          |
| `--scs-molten-amber` | `#D98E32` | Primary text / foreground     |
| `--scs-steel-blue`   | `#4B7EB0` | Borders, accents, status bar  |
| `--scs-liquid-cool`  | `#8BE9FD` | Focus / cyan                  |
| `--scs-radium-green` | `#50FA7B` | Success state                 |
| `--scs-red-oxide`    | `#FF5C5C` | Error state                   |
| (chrome white)       | `#E6E6F0` | Secondary text                |
| (muted)              | `#6272A4` | Disabled / dim foreground     |

When adding a new theme target, translate these exact hex values into the platform's color format. Cross-check existing themes (`Editors/VSCode/spacecraft-software-theme/themes/Spacecraft-Software-color-theme.json`, `Desktops/KDE_Plasma/Spacecraft-Software.colors`, `Bootloaders/ZAMAK/theme.toml`) for proven role mappings before inventing new ones.

**Known exceptions**: two targets intentionally diverge from the canonical Void Navy palette and should not be "fixed" without a reason:
- `CLIs/Claude_Code/` uses a CLI-tuned variant (`#0E141D` bg, `#F0F0F0` fg, `#FE6B00` accent) for terminal legibility.
- The browser themes use the `#FE6B00` "Steel Orange" accent variant for chrome contrast.

## Adding a new theme target

1. Create `<Category>/<TargetName>/` (Editors, Terminals, Desktops, Shells, Browsers, CLIs, AI, or Bootloaders).
2. Write the theme in the target's native config format using the palette above.
3. Add an `INSTALL.md` in that folder — model it after `Editors/VSCode/INSTALL.md` or `Browsers/INSTALL.md` (header line with `**Version:** 1.0 | **Author:** Mohamed Hammad | **License:** GPL3+ | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)`).
4. If the platform consumes a zip/tarball/xpi/vsix, build that archive from the source folder and place it alongside.
5. Update the relevant section of `README.md` if the new target needs a top-level mention.

## Contribution rules (from CONTRIBUTING.md) — enforce these on every change

These constraints apply to any code or config you write here:

- **License**: GPLv3+. Every new source file gets an SPDX header in the appropriate comment syntax: `SPDX-License-Identifier: GPL-3.0-or-later`.
- **POSIX shell only**: Shell scripts must run under `sh`/`dash`. No bashisms (`[[ ]]`, `(( ))`, arrays, `function` keyword, process substitution). The exception is per-shell modules under `Shells/<ShellName>/`, which target that specific shell.
- **Rust**: If Rust ever appears here, follow the [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines). Memory-safety is non-negotiable; ASLR + CFI for any non-Rust language.
- **Dates**: ISO 8601 (`YYYY-MM-DD`, `HH:MM:SS`). Metric units only.
- **Privacy-Friendly App rules**: No telemetry, analytics, ads, tracking, or remote calls in any script or extension. Local storage only.
- **Fonts**: Only OFL / Apache / Ubuntu Font License / CC0 fonts. JetBrains Mono is the safe default for monospace.
- **Accessibility**: Color choices must hold WCAG contrast against the Void Navy background.
- **Keybindings**: Anything with shortcuts must support both CUA (`Ctrl+C/V/S`) and Vim-style (`h/j/k/l`) navigation.

## Editing conventions

- Editing the unpacked theme source does **not** automatically rebuild the sibling archive. Treat the `.zip`/`.tar.gz`/`.xpi`/`.vsix` files as stale until repackaged. When you ship a change, rebuild the matching archive in the same commit.
- The Anthropic `.skill` files in `AI/Claude/` are zip archives (binary). Currently two are shipped (`spacecraft-brand-guidelines`, `spacecraft-theme-factory`); a third, `spacecraft-document-format`, was removed in `edc72a7` and is not in scope here. Edit the unpacked sibling directory of the same name, not the `.skill` file.
- Image assets (`background.png`, `icon.png`, `Spacecraft_Software_wallpaper_blue.png`) are duplicated across `Desktops/*/` folders by design — each desktop ships a self-contained bundle.
- The Claude Code-specific theme (`CLIs/Claude_Code/`) ships a `settings.json` fragment intended to be merged into the user's `~/.claude/settings.json`, not copied wholesale.
- The repo is ~700 MB of working tree (mostly pre-built archives and PNG assets). `git push` over SSH for a fresh clone takes several minutes; budget for that, don't assume the command hung.
- **Upstream-preset adaptation pattern**: when a target already has a high-quality community preset (Starship, oh-my-posh, p10k, etc.), don't author from scratch — port the preset verbatim and substitute its named palette with one mapping every role key to a Spacecraft Software token. `Shells/Starship/starship.toml` is the reference example: it preserves the catppuccin-powerline format string and every module config, but renames `[palettes.catppuccin_mocha]` → `[palettes.spacecraft_software]` and remaps each catppuccin role (`red`, `peach`, `yellow`, `green`, `sapphire`, `lavender`, `crust`, …) to a Spacecraft Software hex. Keep the original role keys so the preset's format string doesn't need to be touched.
