# Spacecraft Software — Windows Desktop Theme

**Version:** 1.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [SpacecraftSoftware.org](https://SpacecraftSoftware.org)

---

## Files included

| File | Purpose |
|---|---|
| `Spacecraft-Software.theme` | Main theme definition (INI format per MS spec) |
| `Spacecraft_Software_wallpaper_blue.png` | Spacecraft Software wallpaper |
| `Spacecraft-Software-icon.png` | Spacecraft Software logo / icon |
| `Spacecraft_Software_dark.reg` | Registry tweak — enforces system-wide Dark mode |
| `Spacecraft_Software_CMD.reg` | Registry tweak — Spacecraft Software colors for `cmd.exe` |

---

## Installation

> **Requirements:** Windows 10 or Windows 11. Administrator rights are needed for the registry tweaks.

### Step 1 — Copy theme files

Theme files can be installed in one of two locations:

**Option A — Current user only** *(recommended, no admin needed for the .theme file)*

```
%LOCALAPPDATA%\Microsoft\Windows\Themes\Spacecraft Software\
```

Copy `Spacecraft-Software.theme` and `Spacecraft_Software_wallpaper_blue.png` into that folder.

**Option B — All users** *(requires admin)*

```
%WinDir%\Resources\Themes\Spacecraft Software\
```

Copy `Spacecraft-Software.theme` and `Spacecraft_Software_wallpaper_blue.png` into that folder.

### Step 2 — Apply the theme

Double-click `Spacecraft-Software.theme`. Windows will open **Settings → Personalization → Themes** and activate Spacecraft Software automatically.

Alternatively:

1. Go to **Settings → Personalization → Themes**.
2. Select **Spacecraft Software** from the list.

### Step 3 — Apply Dark Mode (registry)

Double-click `Spacecraft_Software_dark.reg` and accept the UAC prompt. This sets:

- System apps → **Dark**
- App theme → **Dark**

A sign-out / sign-in may be required for the change to take full effect.

### Step 4 — Apply CMD colors (optional)

Double-click `Spacecraft_Software_CMD.reg` and accept the UAC prompt.  
This sets the default `cmd.exe` console colors to the Spacecraft Software palette.

---

## Accent color

The `.theme` file sets the Aero colorization to **Steel Blue `#4B7EB0`** automatically.

To set it manually:

1. **Settings → Personalization → Colors**
2. Toggle **Custom color** under *Accent color*
3. Enter `#4B7EB0`

---

## Packaging as a .themepack

A `.themepack` is a renamed `.cab` archive that bundles the theme files for distribution.

```powershell
# Run in the Theme\Desktops\Windows\ folder (PowerShell, no admin needed)
$files = @(
    "Spacecraft-Software.theme",
    "Spacecraft_Software_wallpaper_blue.png",
    "Spacecraft-Software-icon.png"
)
$files | ForEach-Object { Copy-Item $_ "$env:TEMP\spacecraft_software_pack\" }
Push-Location "$env:TEMP\spacecraft_software_pack"
makecab /D CompressionType=LZX /D Cabinet=ON /D Compress=ON `
    /D MaxDiskSize=0 /F spacecraft-software.ddf
Move-Item spacecraft-software.cab "$PSScriptRoot\Spacecraft-Software.themepack"
Pop-Location
```

Or simply:

```powershell
# Quick method using Compress-Archive + rename (ZIP-based, works on all Win 10/11)
Compress-Archive -Path Spacecraft-Software.theme, Spacecraft_Software_wallpaper_blue.png, Spacecraft-Software-icon.png `
    -DestinationPath Spacecraft-Software.zip -Force
Rename-Item Spacecraft-Software.zip Spacecraft-Software.themepack
```

Double-clicking `Spacecraft-Software.themepack` will install the theme automatically via Windows.

---

## Uninstalling

1. Go to **Settings → Personalization → Themes**.
2. Switch to a different theme.
3. Delete the `Spacecraft Software\` folder from whichever location you used in Step 1.
4. To revert the registry tweaks, open **Registry Editor** and delete the keys applied by `Spacecraft_Software_dark.reg` and `Spacecraft_Software_CMD.reg`, or re-run them with `DefaultValue=` set to the original values.
