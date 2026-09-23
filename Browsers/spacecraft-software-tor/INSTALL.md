# Installing Spacecraft Software Theme for Tor Browser

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

Every registered Steelbore palette family theme ships as its own WebExtension
theme manifest under `themes/<slug>/manifest.json`, plus a matching one-theme
`themes/tor-<slug>.xpi` archive. `steelbore` (Steelbore Modern) is the
default; pick any other theme the same way.

## Method 1: Install from XPI (Recommended)

1. Open Tor Browser.
2. Navigate to `about:addons` (or press `Ctrl+Shift+A`).
3. Click the gear icon ⚙️ → **Install Add-on From File…**
4. Select `themes/tor-steelbore.xpi` (or another theme's `.xpi`).
5. Click **Add** when prompted.

## Method 2: Temporary Installation (Developer)

1. Open Tor Browser and navigate to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…**
3. Select `themes/<slug>/manifest.json` — e.g. `themes/steelbore/manifest.json`.
4. The theme will be applied immediately (until browser restart).

## Choosing a theme

| Slug | Theme | Notes |
|------|-------|-------|
| `steelbore` | Steelbore | default, dark |
| `steelbore-high-contrast` | Steelbore High Contrast | §11.1.1 accessible-mode sibling |
| `steelbore-blue`, `steelbore-magnetar`, `steelbore-biolume`, `tokyonight`, `steelbore-hanzosteel`, `steelbore-blackpinkpanther`, `steelbore-green`, `steelbore-greenalt`, `steelbore-classic` | alternate palettes (§11.3) | each has a `-high-contrast` sibling too |
| `steelbore-navywhite` | Steelbore NavyWhite | light canvas |
| `solarized-dark`, `solarized-light` | Solarized | §11.5 fidelity palette — reproduced verbatim, **non-conforming**, not adoptable as a project palette |

`steelbore-mono` is not shipped here — Gecko's `theme.colors` is a hex-only
field and cannot express the 4-bit ANSI mono variant.

## Notes

- Tor Browser is based on Firefox ESR and supports WebExtension theme APIs.
- This theme changes only the visual appearance — it does not affect Tor's
  privacy or security features.
