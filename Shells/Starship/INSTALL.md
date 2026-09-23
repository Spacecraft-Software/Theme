# Installing the Spacecraft Software theme for Starship

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Starship configuration per registered theme of the
Steelbore palette family (The Steelbore Standard §11). Each `themes/<slug>.toml`
is the official [catppuccin-powerline](https://starship.rs/presets/catppuccin-powerline)
preset — the Powerline segment layout, module set and icons are untouched —
with its `[palettes.spacecraft_software]` table remapped so every segment
colour resolves to a role token (background, accent, structure, success,
error, focus) instead of a Catppuccin hue. `steelbore.toml` is the default;
every conforming palette also ships a `-high-contrast` sibling for accessible
mode, `steelbore-navywhite.toml` is the family's light canvas,
`steelbore-mono.toml` uses Starship's own ANSI colour names (`black`, `red`,
`green`, `yellow`, `blue`, `cyan`, `white`, `bright-white`) for `NO_COLOR`
sessions, and `solarized-dark.toml` / `solarized-light.toml` are §11.5
**fidelity palettes**: reproduced verbatim from upstream Solarized,
non-conforming, not adoptable as a project palette. All files are generated
from `Steelbore/steelbore.toml` — do not edit them by hand.

## Installation

1. Copy the theme you want to Starship's config path:
   ```sh
   cp themes/steelbore.toml ~/.config/starship.toml
   ```
2. Open a new shell to see it applied.

To follow the system-wide theme declaration (§11.6) instead of a fixed name,
point `STARSHIP_CONFIG` at the slug carried by `SPACECRAFT_THEME`:

```sh
dir="$HOME/.config/spacecraft-software/starship"
export STARSHIP_CONFIG="$dir/${SPACECRAFT_THEME:-steelbore}.toml"
```

(copy `themes/` to that `dir` first, or point `STARSHIP_CONFIG` straight at
this package's `themes/` directory).

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.toml` | Steelbore Modern | **default** |
| `steelbore-high-contrast.toml` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.toml`, `steelbore-magnetar.toml`, `steelbore-biolume.toml`, `tokyonight.toml`, `steelbore-hanzosteel.toml`, `steelbore-blackpinkpanther.toml`, `steelbore-green.toml`, `steelbore-greenalt.toml` | alternates (§11.3) | each with a `-high-contrast.toml` sibling |
| `steelbore-navywhite.toml` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.toml` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.toml`, `solarized-light.toml` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |
| `steelbore-mono.toml` | — | Starship ANSI colour names only, for `NO_COLOR` sessions |
