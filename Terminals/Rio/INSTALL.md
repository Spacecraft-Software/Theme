# Installing Spacecraft Software Theme for Rio Terminal

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Installation

1. Copy any theme from `themes/` to your Rio themes directory:
   - **Linux/macOS:** `~/.config/rio/themes/`
   - **Windows:** `%APPDATA%\rio\themes\`
   
   For example, to install the default Steelbore theme:
   ```sh
   cp themes/steelbore.toml ~/.config/rio/themes/steelbore.toml
   ```

2. In your Rio config (`config.toml`), set:
   ```toml
   theme = "steelbore"
   ```

3. Restart Rio.

## Choosing a Theme

The generator produces 24 colour themes (13 palettes, 2 variants each) plus mono:

| Theme | Canvas | Use Case |
|-------|--------|----------|
| `steelbore` | Dark Navy | Default, Spacecraft Software brand |
| `steelbore-high-contrast` | Dark Navy | Accessible variant of default |
| `steelbore-blue`, `-high-contrast` | Dark Navy | Electric Blue accent variant |
| `steelbore-magnetar`, `-high-contrast` | Dark Navy | Magenta-dominant variant |
| `steelbore-biolume`, `-high-contrast` | Dark Navy | Cyan-heavy variant |
| `steelbore-navywhite`, `-high-contrast` | **Light** | Light canvas variant |
| `steelbore-classic`, `-high-contrast` | Dark Navy | Legacy six-role variant (§11.2) |
| `tokyonight`, `-high-contrast` | Dark Navy | Alternate palette |
| `steelbore-hanzosteel`, `-high-contrast` | Dark Navy | Alternate palette |
| `steelbore-blackpinkpanther`, `-high-contrast` | Dark Navy | Alternate palette |
| `steelbore-green`, `-high-contrast` | Dark Navy | Alternate palette |
| `steelbore-greenalt`, `-high-contrast` | Dark Navy | Alternate palette |
| `solarized-dark`, `solarized-light` | Dark / **Light** | FIDELITY palette (non-conforming; reproduced verbatim) |

All themes adhere to The Steelbore Standard §11 (WCAG 2.2 AA verified) except Solarized, which is a non-conforming fidelity palette provided for compatibility.
