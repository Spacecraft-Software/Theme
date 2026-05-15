# Installing Spacecraft Software Theme for Tor Browser

**Version:** 1.0 | **Author:** Mohamed Hammad | **License:** GPL3+ | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

## Method 1: Install from XPI (Recommended)

1. Open Tor Browser.
2. Navigate to `about:addons` (or press `Ctrl+Shift+A`).
3. Click the gear icon ⚙️ → **Install Add-on From File…**
4. Select the `spacecraft-software-tor-theme.xpi` file.
5. Click **Add** when prompted.

## Method 2: Temporary Installation (Developer)

1. Open Tor Browser and navigate to `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…**
3. Select the `manifest.json` file from the `spacecraft-software-tor/` folder.
4. The theme will be applied immediately (until browser restart).

## Notes

- Tor Browser is based on Firefox ESR and supports WebExtension theme APIs.
- This theme changes only the visual appearance — it does not affect Tor's privacy or security features.
