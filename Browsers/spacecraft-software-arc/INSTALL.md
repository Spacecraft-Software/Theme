# Installing Spacecraft Software Theme for Arc Browser

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

Every registered Steelbore theme ships as its own MV3 theme manifest under
`themes/<slug>/manifest.json`. Arc is Chromium-based and installs exactly
one theme per extension, so each theme is its own loadable folder and its
own zip.

## Method 1: Load as Unpacked Extension

1. Open Arc.
2. Navigate to `arc://extensions` (or `chrome://extensions`).
3. Enable **Developer mode** (toggle in the top-right corner).
4. Click **Load unpacked**.
5. Select the `themes/<slug>/` folder for the theme you want — `themes/steelbore/` for the default.
6. The theme is applied immediately.

## Method 2: Drag and Drop ZIP

1. Open Arc and navigate to `arc://extensions`.
2. Enable **Developer mode**.
3. Drag and drop `themes/spacecraft-software-arc-<slug>.zip` onto the page.

## Method 3: Arc's Built-in Themes (Alternative)

Arc has its own theming system via **Spaces** and **Boosts**:

1. Right-click any Space in the sidebar → **Edit Space**.
2. Under **Theme**, select a base that matches your chosen theme's polarity
   (dark for every theme except `steelbore-navywhite` and `solarized-light`).
3. Set the background to the `background.png` wallpaper from this folder.
4. For an exact accent match, read the `toolbar_text`/`ntp_link` colour out
   of your chosen theme's `themes/<slug>/manifest.json` and set it as the
   Space's accent colour.

## Notes

- For the deepest customization, combine the extension with Arc's built-in
  Boost and Space features.

## Choosing a theme

| Theme | Notes |
|-------|-------|
| `steelbore` | **default** |
| `steelbore-high-contrast` | accessible-mode sibling (§18.1) |
| `steelbore-blue`, `-magnetar`, `-biolume`, `-navywhite`, `tokyonight`, `-hanzosteel`, `-blackpinkpanther`, `-green`, `-greenalt` | nine alternates, each with a `-high-contrast` sibling |
| `steelbore-classic` | legacy six-role palette (§11.2), with a `-high-contrast` sibling |
| `solarized-dark`, `solarized-light` | **fidelity palette (§11.5) — non-conforming**, shipped for interoperability only, no high-contrast sibling |

`steelbore` is the default. `steelbore-navywhite` and `solarized-light` are the
family's only light-canvas themes. There is no mono variant here — a Chrome
MV3 theme manifest is hex colours only.
