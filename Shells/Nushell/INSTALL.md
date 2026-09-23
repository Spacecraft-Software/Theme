# Installing the Spacecraft Software theme for Nushell

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Nushell colour-config module per registered theme of the
Steelbore palette family (The Steelbore Standard §11). Each
`themes/<slug>.nu` defines `export def main [] { return { ... } }`, a record
matching the shape Nushell's `$env.config.color_config` expects: the value
colours (`int`, `float`, `date`, `filesize`, `string`, `bool`, ...), the
`header` and `row_index` accents, `search_result`, and the full `shape_*`
syntax-highlighting table. `steelbore.nu` is the default; every conforming
palette also ships a `-high-contrast` sibling for accessible mode,
`steelbore-navywhite.nu` is the family's light canvas, `steelbore-mono.nu`
supports `NO_COLOR` sessions (it sets Nushell's own colour names — `red`,
`green`, `blue`, `purple`, `white`, `default`, ... — instead of hex), and
`solarized-dark.nu` / `solarized-light.nu` are §11.5 **fidelity palettes**:
reproduced verbatim from upstream Solarized, non-conforming, not adoptable
as a project palette. All files are generated from `Steelbore/steelbore.toml`
— do not edit them by hand.

## Installation

1. Copy `themes/` somewhere in your Nushell config, e.g.
   `~/.config/nushell/spacecraft-software/themes/`.
2. Source the theme you want and apply it from your `config.nu`:
   ```nu
   source ~/.config/nushell/spacecraft-software/themes/steelbore.nu
   $env.config.color_config = (main)
   ```
3. Start a new Nushell session (or `source $nu.config-path`) to see it
   applied.

To follow the system-wide theme declaration (§11.6) instead of a fixed name,
resolve the module path from `SPACECRAFT_THEME` before sourcing it:

```nu
let slug = ($env.SPACECRAFT_THEME? | default "steelbore")
let theme_dir = "~/.config/nushell/spacecraft-software/themes" | path expand
nu -c $"source ($theme_dir)/($slug).nu; $env.config.color_config = \(main\)"
```

or, more simply, keep a fixed `use` line in `config.nu` and change the
sourced filename by hand when you switch themes — Nushell's `source` does
not accept a dynamically built path directly, so scripted selection needs
the `nu -c` indirection above or an equivalent wrapper.

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.nu` | Steelbore Modern | **default** |
| `steelbore-high-contrast.nu` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.nu`, `steelbore-magnetar.nu`, `steelbore-biolume.nu`, `tokyonight.nu`, `steelbore-hanzosteel.nu`, `steelbore-blackpinkpanther.nu`, `steelbore-green.nu`, `steelbore-greenalt.nu` | alternates (§11.3) | each with a `-high-contrast.nu` sibling |
| `steelbore-navywhite.nu` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.nu` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.nu`, `solarized-light.nu` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |
| `steelbore-mono.nu` | — | Nushell colour names only (`red`, `green`, `blue`, `white`, `default`), for `NO_COLOR` sessions |
