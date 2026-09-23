# Spacecraft Software for Claude Code

The Steelbore palette family (The Steelbore Standard §11), rendered as a
Claude Code settings fragment and a matching terminal colour scheme — one
pair per registered theme, `steelbore` as the default.

`themes/<slug>/settings.json` and `themes/<slug>/terminal.json` hold each
theme's rendered output; the canonical values behind every role token live
in `Steelbore/steelbore.toml`, never quoted here (§11.4) — see the
`steelbore-color-palette` skill for the full contract. Both files are
produced by `tools/steelbore_themes` from that TOML. Do not edit either by
hand — edit the renderer (`tools/steelbore_themes/renderers/claude_code.py`)
or the TOML upstream and regenerate.

## Choosing a theme

Pick a slug from the table below and use its two files. `steelbore` is the
default; every alternate palette ships a `-high-contrast` sibling (§11.1.1).
`steelbore-mono` has no hex palette and ships `settings.json` only — its
status line falls back to 4-bit ANSI codes, deferring hue to the terminal
(`NO_COLOR`). Solarized Dark/Light are §11.5 fidelity palettes, reproduced
verbatim and **not conforming** — they are not adoptable as a project theme.

| Theme | Slug | Canvas |
|-------|------|--------|
| **Steelbore** (default) | `steelbore` | Dark |
| Steelbore High Contrast | `steelbore-high-contrast` | Dark |
| Steelbore Blue(-high-contrast) | `steelbore-blue` | Dark |
| Steelbore Magnetar(-high-contrast) | `steelbore-magnetar` | Dark |
| Steelbore Biolume(-high-contrast) | `steelbore-biolume` | Dark |
| Steelbore NavyWhite(-high-contrast) | `steelbore-navywhite` | Light |
| Tokyo Night(-high-contrast) | `tokyonight` | Dark |
| Steelbore Hanzo Steel(-high-contrast) | `steelbore-hanzosteel` | Dark |
| Steelbore BlackPinkPanther(-high-contrast) | `steelbore-blackpinkpanther` | Dark |
| Steelbore Green(-high-contrast) | `steelbore-green` | Dark |
| Steelbore Green Alt(-high-contrast) | `steelbore-greenalt` | Dark |
| Steelbore Classic(-high-contrast) | `steelbore-classic` | Dark |
| Solarized Dark / Light — **fidelity, non-conforming** | `solarized-dark` / `solarized-light` | Dark / Light |
| Steelbore Mono (`settings.json` only) | `steelbore-mono` | — |

## Installation

### 1. Terminal setup (Windows Terminal shown; any scheme-based terminal works)

1. Open Windows Terminal **Settings** → **Color schemes** → **Add new**.
2. Copy the contents of `themes/<slug>/terminal.json` into the configuration.
3. Set the scheme's `name` (e.g. **Steelbore**) as the active scheme for the
   profile you use with Claude Code.

### 2. Claude Code setup

The `settings.json` under each theme's folder is a **fragment** — merge it
into your own config, do not overwrite it wholesale:

1. Open (or create) `~/.claude/settings.json` (`%USERPROFILE%\.claude\settings.json`
   on Windows).
2. Merge in the `statusLine` and `theme` keys from
   `themes/<slug>/settings.json`.
3. If colours look washed out, ensure `COLORTERM=truecolor` is set in your
   environment — the status line's model name and context-window percentage
   are painted with 24-bit truecolor escapes built from the theme's `accent`
   and `structure` roles (4-bit ANSI codes for `steelbore-mono`).

## Environment variable

On supported shells and terminal multiplexers, set `SPACECRAFT_THEME=<slug>`
to switch themes programmatically.
