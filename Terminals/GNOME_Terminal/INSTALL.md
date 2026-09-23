# Installing Spacecraft Software Theme for GNOME Terminal

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Layout

Every theme is a standalone installer script under `themes/`, one per Steelbore
palette-family theme, named by its slug:

```
themes/<slug>.sh
```

Each script is generated (never hand-edit one — edit the renderer at
`tools/steelbore_themes/renderers/gnome_terminal.py` and regenerate) and
creates its own GNOME Terminal profile via `dconf`, named after the theme
(e.g. "Steelbore", "Steelbore High Contrast", "Tokyo Night").

**Requires:** `dconf` and `uuidgen`. If `uuidgen` is not installed, the
script falls back to a checksum-derived id so it still runs.

## Installation

1. Make the script for the theme you want executable and run it:
   ```bash
   chmod +x themes/steelbore.sh
   ./themes/steelbore.sh
   ```
2. Open GNOME Terminal → **Preferences** → **Profiles** → select the new
   profile (its visible name matches the theme name printed by the script).
3. Repeat for any other theme you want available as a separate profile.

Each script only *adds* a profile; it never removes or edits one from an
earlier run. GNOME Terminal keys profiles by UUID, not by visible name, so
running the same script twice creates two distinct profiles with the same
visible name — the script warns to stderr when it detects this, but still
creates the new profile (idempotent-ish, not idempotent). Delete unwanted
duplicates from **Preferences → Profiles**.

## Choosing a theme

`steelbore` is the default and recommended starting point. Every conforming
theme also ships a `-high-contrast` sibling with the same hues raised to a
higher-contrast reading, for accessibility (§11.1.1).

| Slug | Theme | Canvas |
|---|---|---|
| `steelbore` | Steelbore (default) | dark |
| `steelbore-high-contrast` | Steelbore High Contrast | dark |
| `steelbore-blue` / `-high-contrast` | Steelbore Blue | dark |
| `steelbore-magnetar` / `-high-contrast` | Steelbore Magnetar | dark |
| `steelbore-biolume` / `-high-contrast` | Steelbore Biolume | dark |
| `steelbore-navywhite` / `-high-contrast` | Steelbore NavyWhite | **light** |
| `tokyonight` / `-high-contrast` | Tokyo Night | dark |
| `steelbore-hanzosteel` / `-high-contrast` | Steelbore Hanzo Steel | dark |
| `steelbore-blackpinkpanther` / `-high-contrast` | Steelbore BlackPinkPanther | dark |
| `steelbore-green` / `-high-contrast` | Steelbore Green | dark |
| `steelbore-greenalt` / `-high-contrast` | Steelbore Green Alt | dark |
| `steelbore-classic` / `-high-contrast` | Steelbore Classic (legacy six-role) | dark |
| `solarized-dark` | Solarized Dark | dark |
| `solarized-light` | Solarized Light | **light** |

`solarized-dark` / `solarized-light` are a **non-conforming fidelity
palette** (§11.5): reproduced verbatim from upstream Solarized rather than
derived from the Steelbore role contract, and not adoptable as a project
palette elsewhere.

There is no `steelbore-mono` script here — GNOME Terminal's profile colour
keys are hex-only, so the 4-bit ANSI mono variant cannot be expressed in
this format.

GNOME Terminal has no per-profile light/dark flag; a light theme's profile
is simply written with a light background and dark foreground, which is all
GNOME Terminal reads.
