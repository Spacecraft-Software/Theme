# Steelbore — Windows Desktop Theme

**Version:** 1.0 | **Author:** Mohamed Hammad | **License:** GPL-3.0-or-later | **Website:** [steelbore.com](https://steelbore.com)

---

## Files included

| File | Purpose |
|---|---|
| `Steelbore.theme` | Main theme definition (INI format per MS spec) |
| `Steelbore_wallpaper_blue.png` | Steelbore wallpaper |
| `Steelbore-icon.png` | Steelbore logo / icon |
| `Steelbore_dark.reg` | Registry tweak — enforces system-wide Dark mode |
| `Steelbore_CMD.reg` | Registry tweak — Steelbore colors for `cmd.exe` |

---

## Installation

> **Requirements:** Windows 10 or Windows 11. Administrator rights are needed for the registry tweaks.

### Step 1 — Copy theme files

Theme files can be installed in one of two locations:

**Option A — Current user only** *(recommended, no admin needed for the .theme file)*

```
%LOCALAPPDATA%\Microsoft\Windows\Themes\Steelbore\
```

Copy `Steelbore.theme` and `Steelbore_wallpaper_blue.png` into that folder.

**Option B — All users** *(requires admin)*

```
%WinDir%\Resources\Themes\Steelbore\
```

Copy `Steelbore.theme` and `Steelbore_wallpaper_blue.png` into that folder.

### Step 2 — Apply the theme

Double-click `Steelbore.theme`. Windows will open **Settings → Personalization → Themes** and activate Steelbore automatically.

Alternatively:

1. Go to **Settings → Personalization → Themes**.
2. Select **Steelbore** from the list.

### Step 3 — Apply Dark Mode (registry)

Double-click `Steelbore_dark.reg` and accept the UAC prompt. This sets:

- System apps → **Dark**
- App theme → **Dark**

A sign-out / sign-in may be required for the change to take full effect.

### Step 4 — Apply CMD colors (optional)

Double-click `Steelbore_CMD.reg` and accept the UAC prompt.  
This sets the default `cmd.exe` console colors to the Steelbore palette.

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
    "Steelbore.theme",
    "Steelbore_wallpaper_blue.png",
    "Steelbore-icon.png"
)
$files | ForEach-Object { Copy-Item $_ "$env:TEMP\steelbore_pack\" }
Push-Location "$env:TEMP\steelbore_pack"
makecab /D CompressionType=LZX /D Cabinet=ON /D Compress=ON `
    /D MaxDiskSize=0 /F steelbore.ddf
Move-Item steelbore.cab "$PSScriptRoot\Steelbore.themepack"
Pop-Location
```

Or simply:

```powershell
# Quick method using Compress-Archive + rename (ZIP-based, works on all Win 10/11)
Compress-Archive -Path Steelbore.theme, Steelbore_wallpaper_blue.png, Steelbore-icon.png `
    -DestinationPath Steelbore.zip -Force
Rename-Item Steelbore.zip Steelbore.themepack
```

Double-clicking `Steelbore.themepack` will install the theme automatically via Windows.

---

## Uninstalling

1. Go to **Settings → Personalization → Themes**.
2. Switch to a different theme.
3. Delete the `Steelbore\` folder from whichever location you used in Step 1.
4. To revert the registry tweaks, open **Registry Editor** and delete the keys applied by `Steelbore_dark.reg` and `Steelbore_CMD.reg`, or re-run them with `DefaultValue=` set to the original values.
