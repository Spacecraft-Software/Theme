# Installing the Spacecraft Software C shell prompt theme

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one csh/tcsh prompt module per registered theme of the Steelbore
palette family (The Steelbore Standard §11). Each `themes/<slug>.csh` sets colour
variables as truecolor or 4-bit ANSI SGR sequences (wrapped in `%{ %}` for csh
prompt expansion), constructing a prompt that colours the current directory from
the theme's `structure` role and the prompt character from the `text_safe_accent`
role. The file is meant to be **sourced**, not executed — it carries no shebang
and configures only the `prompt` variable. `steelbore.csh` is the default; every
conforming palette also ships a `-high-contrast` sibling for accessible mode, and
`steelbore-mono.csh` uses plain 4-bit ANSI codes for `NO_COLOR` sessions. All
files are generated from `Steelbore/steelbore.toml` — do not edit them.

## Installation

1. Copy `themes/` to `~/.config/spacecraft-software/themes/`.
2. Source the theme you want from `~/.cshrc`:
   ```csh
   source ~/.config/spacecraft-software/themes/steelbore.csh
   ```
3. Open a new shell (or `source ~/.cshrc`) to see it applied.

To follow the system-wide theme declaration (§11.6) instead of a fixed name,
source the slug carried by `SPACECRAFT_THEME`:

```csh
if ( -n "$SPACECRAFT_THEME" ) then
    source ~/.config/spacecraft-software/themes/$SPACECRAFT_THEME.csh
endif
```

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.csh` | Steelbore Modern | **default** |
| `steelbore-high-contrast.csh` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.csh`, `steelbore-magnetar.csh`, `steelbore-biolume.csh`, `tokyonight.csh`, `steelbore-hanzosteel.csh`, `steelbore-blackpinkpanther.csh`, `steelbore-green.csh`, `steelbore-greenalt.csh` | alternates (§11.3) | each with a `-high-contrast.csh` sibling |
| `steelbore-navywhite.csh` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.csh` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.csh`, `solarized-light.csh` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |
| `steelbore-mono.csh` | — | plain 4-bit ANSI codes only, for `NO_COLOR` sessions |
