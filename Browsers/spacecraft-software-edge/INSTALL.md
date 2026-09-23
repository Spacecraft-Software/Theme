# Installing Spacecraft Software Theme for Microsoft Edge

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

Every registered Steelbore theme ships as its own MV3 theme manifest under
`themes/<slug>/manifest.json`. Edge installs exactly one theme per
extension, so each theme is its own loadable folder and its own zip.

## Method 1: Load as Unpacked Extension (Developer)

1. Open Edge.
2. Navigate to `edge://extensions`.
3. Enable **Developer mode** (toggle in the bottom-left corner).
4. Click **Load unpacked**.
5. Select the `themes/<slug>/` folder for the theme you want — `themes/steelbore/` for the default.
6. The theme is applied immediately.

## Method 2: Drag and Drop ZIP

1. Open Edge and navigate to `edge://extensions`.
2. Enable **Developer mode**.
3. Drag and drop `themes/spacecraft-software-edge-<slug>.zip` onto the page.

## Method 3: Microsoft Edge Add-ons store

1. Package a `themes/<slug>/` folder using Edge's extension tools.
2. Upload to the [Microsoft Edge Add-ons Developer Dashboard](https://partner.microsoft.com/dashboard/microsoftedge).
3. Once approved, users can install directly from the store.

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
