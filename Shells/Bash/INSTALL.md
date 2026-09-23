# Installing the Spacecraft Software Bash prompt theme

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Bash prompt module per registered theme of the Steelbore
palette family (The Steelbore Standard §11). Each `themes/<slug>.sh` defines
`spacecraft_software_prompt`, a `PROMPT_COMMAND` function that colours `PS1`
from that theme's `structure` (current directory), `accent` (git branch),
`success` / `error` (exit-status indicator) roles, plus git branch detection.
The file is meant to be **sourced**, not executed — it carries no shebang and
sets no `LS_COLORS`. `steelbore.sh` is the default; every conforming palette
also ships a `-high-contrast` sibling for accessible mode, and
`steelbore-mono.sh` uses plain 4-bit ANSI codes for `NO_COLOR` sessions. All
files are generated from `Steelbore/steelbore.toml` — do not edit them.

## Installation

1. Copy `themes/` to `~/.config/spacecraft-software/themes/`.
2. Source the theme you want from `~/.bashrc`:
   ```sh
   . ~/.config/spacecraft-software/themes/steelbore.sh
   ```
3. Open a new shell (or `source ~/.bashrc`) to see it applied.

To follow the system-wide theme declaration (§11.6) instead of a fixed name,
source the slug carried by `SPACECRAFT_THEME`:

```sh
dir="$HOME/.config/spacecraft-software"
[ -n "$SPACECRAFT_THEME" ] && . "$dir/themes/$SPACECRAFT_THEME.sh"
```

## Choosing a theme

| File | Palette | Notes |
|------|---------|-------|
| `steelbore.sh` | Steelbore Modern | **default** |
| `steelbore-high-contrast.sh` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue.sh`, `steelbore-magnetar.sh`, `steelbore-biolume.sh`, `tokyonight.sh`, `steelbore-hanzosteel.sh`, `steelbore-blackpinkpanther.sh`, `steelbore-green.sh`, `steelbore-greenalt.sh` | alternates (§11.3) | each with a `-high-contrast.sh` sibling |
| `steelbore-navywhite.sh` | Steelbore NavyWhite | the family's light canvas |
| `steelbore-classic.sh` | Steelbore Classic | the original Void Navy / Molten Amber look (§11.2) |
| `solarized-dark.sh`, `solarized-light.sh` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **not WCAG-conforming** |
| `steelbore-mono.sh` | — | plain 4-bit ANSI codes only, for `NO_COLOR` sessions |
