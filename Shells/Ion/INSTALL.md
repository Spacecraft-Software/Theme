# Spacecraft Software Ion Theme

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

The generated theme files live in the `themes/` directory. Each theme is a standalone `.ion` configuration snippet — source one in your `~/.config/ion/initrc` to activate it.

## Installation

1. Choose a theme from `themes/` (e.g., `themes/steelbore.ion` for the default).
2. Add to your `~/.config/ion/initrc`:

   ```ion
   source /path/to/Shells/Ion/themes/steelbore.ion
   ```

   Or, to enable theme selection by environment variable:

   ```ion
   if set SPACECRAFT_THEME
       source /path/to/Shells/Ion/themes/${SPACECRAFT_THEME}.ion
   else
       source /path/to/Shells/Ion/themes/steelbore.ion
   end
   ```

3. Restart Ion or reload your config (`source ~/.config/ion/initrc`).

## Choosing a Theme

| Theme | Description | Variant |
|-------|-------------|---------|
| `steelbore` | **Default** Steelbore (Modern) | Dark |
| `steelbore-high-contrast` | Steelbore with enhanced contrast | Dark |
| `steelbore-blue` | Steelbore Blue (Electric Blue accent) | Dark |
| `steelbore-blue-high-contrast` | Steelbore Blue HC | Dark |
| `steelbore-magnetar` | Steelbore Magnetar (Hot accent) | Dark |
| `steelbore-magnetar-high-contrast` | Steelbore Magnetar HC | Dark |
| `steelbore-biolume` | Steelbore Biolume (Teal accent) | Dark |
| `steelbore-biolume-high-contrast` | Steelbore Biolume HC | Dark |
| `steelbore-navywhite` | **Light canvas** Navy on White | Light |
| `steelbore-navywhite-high-contrast` | Steelbore NavyWhite HC | Light |
| `tokyonight` | Tokyo Night (Community palette) | Dark |
| `tokyonight-high-contrast` | Tokyo Night HC | Dark |
| `steelbore-hanzosteel` | Steelbore Hanzo Steel (Cyan accent) | Dark |
| `steelbore-hanzosteel-high-contrast` | Steelbore Hanzo Steel HC | Dark |
| `steelbore-blackpinkpanther` | Steelbore BlackPinkPanther (Hot Pink accent) | Dark |
| `steelbore-blackpinkpanther-high-contrast` | Steelbore BlackPinkPanther HC | Dark |
| `steelbore-green` | Steelbore Green (Green accent) | Dark |
| `steelbore-green-high-contrast` | Steelbore Green HC | Dark |
| `steelbore-greenalt` | Steelbore Green Alt (Alt Green accent) | Dark |
| `steelbore-greenalt-high-contrast` | Steelbore Green Alt HC | Dark |
| `steelbore-classic` | Steelbore Classic (Legacy 6-role) | Dark |
| `steelbore-classic-high-contrast` | Steelbore Classic HC | Dark |
| `solarized-dark` | **Fidelity palette** (non-conforming) | Dark |
| `solarized-light` | **Fidelity palette** (non-conforming) | Light |
| `steelbore-mono` | Steelbore Mono (4-bit ANSI, NO_COLOR) | Mono |

### About High-Contrast Variants

High-contrast themes (denoted `-high-contrast` suffix) follow The Steelbore Standard §11.1.1 and offer enhanced contrast for improved accessibility. They use the same palette family but with lifted accent and structure colours.

### About Solarized

The Solarized themes are **fidelity palettes** that reproduce Ethan Schoonover's Solarized verbatim. They do not conform to The Steelbore Standard's palette contract and are not recommended as new project palettes — they are provided for compatibility and migration.

### About Mono

The `steelbore-mono` theme uses only standard ANSI colour names (no hex). It respects the `NO_COLOR` environment variable and defers hue selection to your terminal configuration, making it compatible with any terminal colour scheme.

## Theme Variables

Every theme exports these Ion shell variables:

- `background` — canvas fill
- `foreground` — body text
- `accent` — primary UI accent
- `structure` — borders, comments, secondary text
- `success` — success state, strings
- `error` — error state, destructive actions
- `warning` — warning / attention
- `focus` — focus state, active element

The prompt function uses `structure` for the directory, `success` for a successful exit (green ❯), and `error` for a failed exit (red ❯).

## Configuration

To apply a theme:

```bash
export SPACECRAFT_THEME=steelbore
# Reload Ion config:
source ~/.config/ion/initrc
```

For permanent configuration, add to `~/.config/ion/initrc`:

```ion
set SPACECRAFT_THEME steelbore
```

## Learn More

- [Ion Shell](https://github.com/redox-os/ion) — the Ion shell repository
- [The Steelbore Standard](https://Steelbore.SpacecraftSoftware.org/) — palette contract and conformance rules
- [Spacecraft Software Themes](https://Theme.SpacecraftSoftware.org/) — theme repository
