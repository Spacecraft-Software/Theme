# Installing Spacecraft Software Theme for Azure DevOps

**Version:** 2.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

`themes/` holds one Azure DevOps `ms.vss-web.theme` contribution per
registered theme of the Steelbore palette family (The Steelbore Standard
§11) — `steelbore.json` is the default, and every conforming palette also
ships a `-high-contrast.json` sibling for accessible mode. `vss-extension.json`
is the full extension manifest: one contribution per theme, ready for
`tfx extension create`. All files are generated from `Steelbore/steelbore.toml`
— do not edit them by hand.

## Method 1: Install from VSIX (Organization)

1. Go to your Azure DevOps organization's **Manage Extensions** page.
2. Click **Browse Marketplace** or **Upload extension**.
3. Upload `SpacecraftSoftware.spacecraft-software-theme-2.0.0.vsix`.
4. Install the extension to your organization.
5. Every theme in the table below becomes available under
   **User Settings → Theme**.

## Method 2: Publish to the Azure DevOps Marketplace

1. Install the `tfx` CLI: `npm install -g tfx-cli`
2. Run `tfx extension create --manifest-globs vss-extension.json` inside this
   folder.
3. Upload the resulting `.vsix` to the
   [Azure DevOps Marketplace](https://marketplace.visualstudio.com/azuredevops).
4. Share or publish for public/private use.

## Method 3: Local Development

1. Install `tfx-cli`: `npm install -g tfx-cli`
2. Package: `tfx extension create --manifest-globs vss-extension.json`
3. Upload the `.vsix` to your Azure DevOps organization for testing.

## Choosing a theme

Every entry in the table is one `themes/<slug>.json` contribution and one
`spacecraft-software-<slug>-theme` id inside `vss-extension.json`.

| Slug | Palette | Notes |
|------|---------|-------|
| `steelbore` | Steelbore Modern | **default** |
| `steelbore-high-contrast` | Steelbore Modern, lifted | accessible mode |
| `steelbore-blue`, `steelbore-magnetar`, `steelbore-biolume`, `tokyonight`, `steelbore-hanzosteel`, `steelbore-blackpinkpanther`, `steelbore-green`, `steelbore-greenalt` | alternates (§11.3) | each with a `-high-contrast` sibling |
| `steelbore-navywhite` | Steelbore NavyWhite | the family's light canvas (`uiTheme: "light"`) |
| `steelbore-classic` | Steelbore Classic | the original six-role look (§11.2) |
| `solarized-dark`, `solarized-light` | Solarized | fidelity palettes (§11.5): reproduced verbatim, **non-conforming, not adoptable as a project palette** |

Azure DevOps has no 4-bit/`NO_COLOR` theme surface, so `steelbore-mono` is not
shipped here.
