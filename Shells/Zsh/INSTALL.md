# Installing the Spacecraft Software Zsh prompt theme

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Zsh prompt module per registered theme of the Steelbore
palette family (The Steelbore Standard §11). Each `themes/<slug>.zsh` sets
up `vcs_info` (branch readout in `accent`, plus a staged/unstaged dirty
indicator in `success`/`warning`), a vi-mode command indicator in `focus`, and
a `PROMPT`/`RPROMPT` pair coloured from that theme's `structure` (current
directory, clock), `success`/`error` (exit-status glyph) and `foreground`
(background-job count) roles. The file is meant to be **sourced**, not
executed — it carries no shebang. `steelbore.zsh` is the default; every
conforming palette also ships a `-high-contrast` sibling for accessible mode,
and `steelbore-mono.zsh` uses plain 4-bit ANSI colour names for `NO_COLOR`
sessions. All files are generated from `Steelbore/steelbore.toml` — do not
edit them.

## Installation

1. Copy `themes/` to `~/.config/spacecraft-software/themes/`.
2. Source the theme you want from `~/.zshrc`:
   ```zsh
   . ~/.config/spacecraft-software/themes/steelbore.zsh
   ```
3. Open a new shell (or `source ~/.zshrc`) to see it applied.

To follow the system-wide theme declaration (§11.6) instead of a fixed name,
source the slug carried by `SPACECRAFT_THEME`:

```zsh
dir="$HOME/.config/spacecraft-software"
[ -n "$SPACECRAFT_THEME" ] && . "$dir/themes/$SPACECRAFT_THEME.zsh"
```

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.zsh` | Steelbore Modern | **default** |
| `steelbore-high-contrast.zsh` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.zsh`, `steelbore-magnetar.zsh`, `steelbore-biolume.zsh`, `tokyonight.zsh`, `steelbore-hanzosteel.zsh`, `steelbore-blackpinkpanther.zsh`, `steelbore-green.zsh`, `steelbore-greenalt.zsh` | alternates (§11.3) | each with a `-high-contrast.zsh` sibling |
| `steelbore-navywhite.zsh` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.zsh` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.zsh`, `solarized-light.zsh` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |
| `steelbore-mono.zsh` | — | plain 4-bit ANSI colour names only, for `NO_COLOR` sessions |
