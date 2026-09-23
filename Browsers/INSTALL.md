# Spacecraft Software Browser Themes — Installation Guide

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

This directory contains Spacecraft Software themes for all supported browsers. Each subfolder has its own `INSTALL.md` with detailed instructions.

---

## 🌐 Chromium-Based Browsers

Every registered theme ships its own MV3 manifest at
`themes/<slug>/manifest.json` and its own installable
`themes/<vendor>-<slug>.zip`; `steelbore` is the default. Chrome (and every
Chromium fork) installs exactly one theme per extension, so pick the
`<slug>` folder or zip for the theme you want — there is no in-browser theme
picker.

### Google Chrome (`spacecraft-software-chrome/`)

1. Open Chrome → `chrome://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select `themes/steelbore/` (or another theme's folder).
3. *Or* drag `themes/spacecraft-software-chrome-steelbore.zip` onto the extensions page.

### Microsoft Edge (`spacecraft-software-edge/`)

1. Open Edge → `edge://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select `themes/steelbore/` (or another theme's folder).
3. *Or* drag `themes/spacecraft-software-edge-steelbore.zip` onto the extensions page.

### Brave (`spacecraft-software-brave/`)

1. Open Brave → `brave://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select `themes/steelbore/` (or another theme's folder).
3. *Or* drag `themes/spacecraft-software-brave-steelbore.zip` onto the extensions page.

### Trivalent (`spacecraft-software-trivalent/`)

1. Open Trivalent → `chrome://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select `themes/steelbore/` (or another theme's folder).
3. *Or* drag `themes/spacecraft-software-trivalent-steelbore.zip` onto the extensions page.

### Arc (`spacecraft-software-arc/`)

1. Open Arc → `arc://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select `themes/steelbore/` (or another theme's folder).
3. *Alternative:* Right-click a Space in the sidebar → **Edit Space** → use `background.png` as wallpaper and match the accent to your chosen theme's manifest.

Every Chromium theme here has a `-high-contrast` sibling per palette, a light
`steelbore-navywhite`, and the §11.5 fidelity pair `solarized-dark` /
`solarized-light` (reproduced verbatim, non-conforming). `steelbore-mono` is
not shipped — an MV3 `theme.colors` block is hex-only.

---

## 🦊 Firefox-Based Browsers

### Mozilla Firefox (`spacecraft-software-firefox/`)

Every registered theme ships its own manifest at `themes/<slug>/manifest.json`
and its own installable `themes/firefox-<slug>.xpi`; `steelbore` is the default.

1. Open Firefox → `about:addons` (`Ctrl+Shift+A`).
2. Gear icon ⚙️ → **Install Add-on From File…** → select `themes/firefox-steelbore.xpi` (or another theme's `.xpi`).
3. *Or* temporary load via `about:debugging#/runtime/this-firefox` → **Load Temporary Add-on** → select `themes/steelbore/manifest.json`.

### Zen Browser (`spacecraft-software-zen/`)

Every registered theme ships its own manifest at `themes/<slug>/manifest.json`
and its own installable `themes/zen-<slug>.xpi`; `steelbore` is the default.

1. Open Zen → `about:addons` (`Ctrl+Shift+A`).
2. Gear icon ⚙️ → **Install Add-on From File…** → select `themes/zen-steelbore.xpi` (or another theme's `.xpi`).
3. *Or* use Zen's native theme settings, matching a theme's accent and canvas manually.

### Tor Browser (`spacecraft-software-tor/`)

Every registered theme ships its own manifest at `themes/<slug>/manifest.json`
and its own installable `themes/tor-<slug>.xpi`; `steelbore` is the default.

1. Open Tor Browser → `about:addons` (`Ctrl+Shift+A`).
2. Gear icon ⚙️ → **Install Add-on From File…** → select `themes/tor-steelbore.xpi` (or another theme's `.xpi`).
3. *Note:* This theme changes only visuals — it does not affect Tor's privacy/security features.

Every Gecko theme has a `-high-contrast` sibling per palette, a light
`steelbore-navywhite`, and the §11.5 fidelity pair `solarized-dark` /
`solarized-light` (reproduced verbatim, non-conforming). `steelbore-mono` is
not shipped — Gecko's `theme.colors` is hex-only.

---

## 🎮 Opera Browsers

### Opera GX (`spacecraft-software-opera-gx/`)

1. Open Opera GX → `opera://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select the `spacecraft-software-opera-gx/` folder.
3. *Or* drag `spacecraft-software-opera-gx.zip` onto the extensions page.
4. *Store upload:* Upload to [GX.store](https://store.gx.me/) as a GX Mod.

### Opera One / Opera Air (`spacecraft-software-opera-one/`)

Every registered theme ships its own MV3 manifest at
`themes/<slug>/manifest.json` and its own installable
`themes/opera-one-<slug>.zip`; `steelbore` is the default.

1. Open Opera One → `opera://extensions` → Enable **Developer mode**.
2. Click **Load unpacked** → select `themes/steelbore/` (or another theme's folder).
3. *Or* drag `themes/spacecraft-software-opera-one-steelbore.zip` onto the extensions page.
4. *Alternative:* Use **Easy Setup** → **Classic** theme → add `background.png` as wallpaper and match your chosen theme's polarity.

### Opera Neon (`spacecraft-software-opera-neon/`)

Opera Neon does not support theme extensions. Apply manually:

1. Go to **Settings** → **Customization** → **Wallpapers** → add `background.png`.
2. Set the accent colour to the theme's `accent` role from `Steelbore/steelbore.json` (Plasma Orange for the default Steelbore palette).
3. See `spacecraft-software-opera-neon/INSTALL.md` for full color reference table.
