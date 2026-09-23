# Spacecraft Software Azure DevOps Theme

The Steelbore palette family (The Steelbore Standard §11), ported to Azure
DevOps boards and pipelines as an `ms.vss-web.theme` extension — one theme
per registered palette, `steelbore` as the default.

`themes/<slug>.json` holds each theme's bare contribution object; the
canonical values behind every role token live in `Steelbore/steelbore.toml`,
never quoted here (§11.4) — see the `steelbore-color-palette` skill for the
full contract. `vss-extension.json` is the generated manifest bundling all of
them; both are produced by `tools/steelbore_themes` from that TOML. Do not
edit either by hand — edit the renderer
(`tools/steelbore_themes/renderers/azuredevops.py`) or the TOML upstream and
regenerate.

## Packaging

To package this extension for your organization:

1. Install `tfx-cli`:
   ```bash
   npm install -g tfx-cli
   ```

2. Package the extension:
   ```bash
   tfx extension create --manifest-globs vss-extension.json
   ```

3. Upload the generated `.vsix` to your [Azure DevOps Marketplace Management console](https://marketplace.visualstudio.com/manage).

See `INSTALL.md` for installing the pre-built
`SpacecraftSoftware.spacecraft-software-theme-2.0.0.vsix` instead, and for the
full theme table.
