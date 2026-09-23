# Installing the Spacecraft Software themes for the Linux console (TTY)

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one POSIX `sh` palette script per registered theme of the
Steelbore palette family (The Steelbore Standard §11). Each script loads its
theme's 16-colour palette into the Linux virtual console via the private
`ESC ] P nc` escape (`console_codes(4)`) and only runs its body when
`$TERM` is `linux` — it is a safe no-op inside any pseudo-terminal (xterm,
tmux, SSH, a graphical terminal emulator, ...). `steelbore.sh` is the
default; every conforming palette also ships a `-high-contrast` sibling for
accessible mode, and `steelbore-mono.sh` supports `NO_COLOR` sessions.
All files are generated from `Steelbore/steelbore.toml` — do not edit them.

## Installation

1. Copy `themes/` somewhere on the console's boot path, e.g.
   `/usr/local/share/spacecraft-software/tty/themes/`.
2. Source the theme you want from a place that runs on every virtual
   console login — `/etc/profile.d/spacecraft-software-tty.sh` for a
   system-wide default, or a line in the console user's own shell profile:
   ```sh
   . /usr/local/share/spacecraft-software/tty/themes/steelbore.sh
   ```
3. Log into (or switch to) a virtual console (`Ctrl+Alt+F<n>`) to see it
   applied; each script re-applies itself on every new login shell.

To follow the system-wide theme declaration (§11.6), source the slug
carried by `SPACECRAFT_THEME` instead of a fixed name:

```sh
. "/usr/local/share/spacecraft-software/tty/themes/${SPACECRAFT_THEME:-steelbore}.sh"
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
| `steelbore-mono.sh` | — | resets attributes only; sets no palette, so the console keeps its own colours (`NO_COLOR`) |
