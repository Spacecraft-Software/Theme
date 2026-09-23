# Installing the Spacecraft Software theme for Fish

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Fish snippet per registered theme of the Steelbore
palette family (The Steelbore Standard §11): the `fish_color_*` and
`fish_pager_color_*` universal variables that drive Fish's syntax
highlighting, selection, search-match and tab-completion pager, plus a
`fish_prompt` function that colours the working directory, the current Git
branch and the last command's exit status. `steelbore.fish` is the
default; every conforming palette also ships a `-high-contrast` sibling for
accessible mode, `steelbore-navywhite.fish` is the family's light canvas,
`steelbore-mono.fish` supports `NO_COLOR` sessions (it sets Fish's own
colour names — `normal`, `blue`, `green`, ... — instead of hex), and
`solarized-dark.fish` / `solarized-light.fish` are §11.5 **fidelity
palettes**: reproduced verbatim from upstream Solarized, non-conforming,
not adoptable as a project palette. All files are generated from
`Steelbore/steelbore.toml` — do not edit them by hand.

## Installation

1. Copy `themes/` somewhere in your Fish config, e.g.
   `~/.config/fish/spacecraft-software/themes/`.
2. Source the theme you want from `~/.config/fish/config.fish`:
   ```fish
   source ~/.config/fish/spacecraft-software/themes/steelbore.fish
   ```
3. Open a new Fish session (or run `source ~/.config/fish/config.fish`) to
   see it applied.

To follow the system-wide theme declaration (§11.6), source the slug
carried by `SPACECRAFT_THEME` instead of a fixed name:

```fish
source ~/.config/fish/spacecraft-software/themes/$SPACECRAFT_THEME.fish
```
or, with a fallback when the variable is unset:
```fish
set -q SPACECRAFT_THEME; or set -g SPACECRAFT_THEME steelbore
source ~/.config/fish/spacecraft-software/themes/$SPACECRAFT_THEME.fish
```

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.fish` | Steelbore Modern | **default** |
| `steelbore-high-contrast.fish` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.fish`, `steelbore-magnetar.fish`, `steelbore-biolume.fish`, `tokyonight.fish`, `steelbore-hanzosteel.fish`, `steelbore-blackpinkpanther.fish`, `steelbore-green.fish`, `steelbore-greenalt.fish` | alternates (§11.3) | each with a `-high-contrast.fish` sibling |
| `steelbore-navywhite.fish` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.fish` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.fish`, `solarized-light.fish` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |
| `steelbore-mono.fish` | — | Fish colour names only (`normal`, `blue`, `green`, `red`, `yellow`, `brwhite`), for `NO_COLOR` sessions |
