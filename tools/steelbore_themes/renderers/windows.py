# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Windows desktop theme, console palette and accent-colour renderer.

Three files per theme, all INI-shaped and comment-friendly with ``;``:

* ``<slug>.theme`` — the desktop theme (cursors, icons, wallpaper reference,
  ``[Control Panel\\Colors]`` and ``[VisualStyles]``). Every non-colour
  section (cursors, icon CLSIDs, wallpaper reference, sounds, slideshow,
  boot, master-theme-selector) is carried over from the legacy hand-written
  file unchanged — those carry no palette colour and are Windows-format
  boilerplate, not theme content.
* ``<slug>-console.reg`` — ``cmd.exe`` / Console-host colour table
  (``ColorTable00``-``ColorTable15``) plus font settings.
* ``<slug>-accent.reg`` — the system light/dark toggle and the DWM accent
  colour.

``[Control Panel\\Colors]`` covers the full documented set of classic Windows
system-colour names (the Win32 ``COLOR_*`` indices), not just the subset the
legacy ``.theme`` carried — every key maps to the closest §11.1 role token,
per ``tools/README.md`` rule 2. ``Hilight`` and ``MenuHilight`` are fills that
carry normal-size text (``HilightText``) directly on top of them, so they use
``theme.text_safe_accent`` rather than the bare accent role (rule 4) — under
Steelbore Blue, plain accent-on-canvas is a restricted (3.91:1) pairing, and
contrast is symmetric, so text drawn in the *background* hue on an accent fill
clears the exact same ratio the restriction exists to avoid.

Every colour is read from :class:`Theme`; a Windows ``.reg`` ``dwordBGR``
value is built from ``theme.rgb()``/``hex_to_rgb`` at render time, never
typed as a literal.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import Theme, hex_to_rgb
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

# [Control Panel\Colors] key -> role token. Plain role lookups only; the
# three accent-highlight keys (Hilight, HilightText, MenuHilight) are handled
# separately in _render_theme_file because they need theme.text_safe_accent.
_COLOR_KEYS: tuple[tuple[str, str], ...] = (
    ("Scrollbar", "background"),
    ("Background", "background"),
    ("ActiveTitle", "surface"),
    ("GradientActiveTitle", "surface"),
    ("InactiveTitle", "background"),
    ("GradientInactiveTitle", "background"),
    ("Menu", "surface"),
    ("MenuBar", "surface"),
    ("Window", "surface-alt"),
    ("WindowFrame", "border"),
    ("MenuText", "foreground"),
    ("WindowText", "foreground"),
    ("TitleText", "foreground"),
    ("ActiveBorder", "border"),
    ("InactiveBorder", "border"),
    ("AppWorkspace", "background"),
    ("ButtonFace", "surface"),
    ("ButtonShadow", "structure"),
    ("GrayText", "structure"),
    ("ButtonText", "foreground"),
    ("InactiveTitleText", "structure"),
    ("ButtonHilight", "border"),
    ("ButtonDkShadow", "structure"),
    ("ButtonLight", "border"),
    ("InfoText", "foreground"),
    ("InfoWindow", "surface"),
    ("HotTrackingColor", "structure"),
)


def _triple(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"{r} {g} {b}"


def _bgr_dword(hex_value: str) -> str:
    """``#RRGGBB`` -> the ``00BBGGRR`` byte order a Console ``ColorTableNN``
    or a DWM ``AccentColor`` dword expects."""
    r, g, b = hex_to_rgb(hex_value)
    return f"{b:02X}{g:02X}{r:02X}"


def _render_theme_file(theme: Theme) -> str:
    """``<slug>.theme`` — INI theme definition."""
    lines: list[str] = [
        theme.header("Windows desktop theme", ";").rstrip("\n"),
        "",
        "[Theme]",
        f"DisplayName={theme.name}",
        "SetLogonBackground=0",
        "",
        "; --- Desktop Icons ----------------------------------------------------",
        "",
        "; Computer - SHIDI_SERVER",
        "[CLSID\\{20D04FE0-3AEA-1069-A2D8-08002B30309D}\\DefaultIcon]",
        "DefaultValue=%SystemRoot%\\System32\\imageres.dll,-109",
        "",
        "; Documents - SHIDI_USERFILES",
        "[CLSID\\{59031A47-3F72-44A7-89C5-5595FE6B30EE}\\DefaultIcon]",
        "DefaultValue=%SystemRoot%\\System32\\shell32.dll,-235",
        "",
        "; Network - SHIDI_MYNETWORK",
        "[CLSID\\{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}\\DefaultIcon]",
        "DefaultValue=%SystemRoot%\\System32\\imageres.dll,-25",
        "",
        "; Recycle Bin - SHIDI_RECYCLERFULL / SHIDI_RECYCLER",
        "[CLSID\\{645FF040-5081-101B-9F08-00AA002F954E}\\DefaultIcon]",
        "Full=%SystemRoot%\\System32\\imageres.dll,-54",
        "Empty=%SystemRoot%\\System32\\imageres.dll,-55",
        "",
        "; --- Cursors ------------------------------------------------------------",
        "",
        "[Control Panel\\Cursors]",
        "AppStarting=%SystemRoot%\\cursors\\aero_working.ani",
        "Arrow=%SystemRoot%\\cursors\\aero_arrow.cur",
        "Crosshair=",
        "Hand=%SystemRoot%\\cursors\\aero_link.cur",
        "Help=%SystemRoot%\\cursors\\aero_helpsel.cur",
        "IBeam=",
        "No=%SystemRoot%\\cursors\\aero_unavail.cur",
        "NWPen=%SystemRoot%\\cursors\\aero_pen.cur",
        "SizeAll=%SystemRoot%\\cursors\\aero_move.cur",
        "SizeNESW=%SystemRoot%\\cursors\\aero_nesw.cur",
        "SizeNS=%SystemRoot%\\cursors\\aero_ns.cur",
        "SizeNWSE=%SystemRoot%\\cursors\\aero_nwse.cur",
        "SizeWE=%SystemRoot%\\cursors\\aero_ew.cur",
        "UpArrow=%SystemRoot%\\cursors\\aero_up.cur",
        "Wait=%SystemRoot%\\cursors\\aero_busy.ani",
        "DefaultValue=Windows Default",
        "DefaultValue.MUI=@main.cpl,-1020",
        "",
        "; --- Desktop / Wallpaper --------------------------------------------------",
        "",
        "[Control Panel\\Desktop]",
        "Wallpaper=Spacecraft_Software_wallpaper_blue.png",
        "TileWallpaper=0",
        "; 10 = Fill (resize and crop to fill screen, maintain ratio) - Windows 7+",
        "WallpaperStyle=10",
        "Pattern=",
        "ScreenSaveActive=0",
        "",
        "; --- System Colors ----------------------------------------------------------",
        "; Applies under Windows Classic / Basic / High Contrast; the active",
        "; Aero.msstyles visual style controls most of these otherwise.",
        "",
        "[Control Panel\\Colors]",
    ]
    for key, role in _COLOR_KEYS:
        lines.append(f"{key}={_triple(theme.rgb(role))}")
    # Highlight fills carry normal-size text directly on top of them; use the
    # text-safe accent (tools/README.md rule 4) rather than the bare accent.
    lines.append(f"Hilight={_triple(hex_to_rgb(theme.text_safe_accent))}")
    lines.append(f"HilightText={_triple(theme.rgb('background'))}")
    lines.append(f"MenuHilight={_triple(hex_to_rgb(theme.text_safe_accent))}")
    lines += [
        "",
        "; --- App Events / Sounds -----------------------------------------------------",
        "; Windows built-in sound scheme; individual events left at default.",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\.Default]",
        "DefaultValue=%WinDir%\\media\\ding.wav",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\AppGPFault]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\Close]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\Maximize]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\MenuCommand]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\MenuPopup]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\Minimize]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\Open]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\RestoreDown]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\RestoreUp]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\RingIn]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\Ringout]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemAsterisk]",
        "DefaultValue=%WinDir%\\media\\chord.wav",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemDefault]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemExclamation]",
        "DefaultValue=%WinDir%\\media\\chord.wav",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemExit]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemHand]",
        "DefaultValue=%WinDir%\\media\\chord.wav",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemQuestion]",
        "DefaultValue=%WinDir%\\media\\chord.wav",
        "",
        "[AppEvents\\Schemes\\Apps\\.Default\\SystemStart]",
        "DefaultValue=",
        "",
        "[AppEvents\\Schemes\\Apps\\Explorer\\EmptyRecycleBin]",
        "DefaultValue=%WinDir%\\media\\ding.wav",
        "",
        "[Sounds]",
        "SchemeName=@%SystemRoot%\\System32\\mmres.dll,-800",
        "",
        "; --- Slideshow -----------------------------------------------------------",
        "; Single static wallpaper - no slideshow rotation.",
        "",
        "[Slideshow]",
        "Interval=1800000",
        "Shuffle=0",
        "ImagesRootPath=",
        "Item0Path=Spacecraft_Software_wallpaper_blue.png",
        "",
        "; --- Screen Saver ---------------------------------------------------------",
        "; Screen savers deprecated from Windows 10 Anniversary Update onward.",
        "",
        "[boot]",
        "SCRNSAVE.EXE=",
        "",
        "; --- Master Theme Selector -------------------------------------------------",
        "; Required. MTSM=DABJDKT marks this as a valid theme file.",
        "",
        "[MasterThemeSelector]",
        "MTSM=DABJDKT",
        "ThemeColorBPP=4",
        "",
        "; --- Visual Styles ----------------------------------------------------------",
        "; Points to Aero.msstyles; ColorizationColor carries the theme's accent.",
        "",
        "[VisualStyles]",
        "Path=%SystemRoot%\\resources\\Themes\\Aero\\Aero.msstyles",
        "ColorStyle=NormalColor",
        "Size=NormalSize",
        "AutoColorization=0",
        f"ColorizationColor=0XC4{theme.hex_bare('accent').upper()}",
        "Transparency=1",
        f"SystemMode={'Light' if theme.is_light else 'Dark'}",
        f"AppMode={'Light' if theme.is_light else 'Dark'}",
        "",
    ]
    return "\n".join(lines) + "\n"


def _render_console_reg(theme: Theme) -> str:
    """``<slug>-console.reg`` — ``cmd.exe`` / Console-host colour table."""
    lines: list[str] = [
        "Windows Registry Editor Version 5.00",
        "",
        theme.header("Windows console colours", ";").rstrip("\n"),
        "",
        "[HKEY_CURRENT_USER\\Console]",
        '"FaceName"="Inconsolata"',
        '"FontFamily"=dword:00000036',
        '"FontWeight"=dword:00000190',
        '"FontSize"=dword:00100000',
        "; ScreenColors: low nibble = background index, high nibble =",
        "; foreground index. Background is always ColorTable00, foreground",
        "; ColorTable07 in the ANSI 16 layout, so this is fixed at 0x07.",
        '"ScreenColors"=dword:00000007',
        "",
    ]
    for index, hex_value in enumerate(theme.ansi16()):
        lines.append(f'"ColorTable{index:02d}"=dword:00{_bgr_dword(hex_value)}')
    lines.append("")
    return "\n".join(lines) + "\n"


def _render_accent_reg(theme: Theme) -> str:
    """``<slug>-accent.reg`` — system light/dark toggle and DWM accent colour."""
    light_dword = "00000001" if theme.is_light else "00000000"
    lines: list[str] = [
        "Windows Registry Editor Version 5.00",
        "",
        theme.header("Windows accent colour", ";").rstrip("\n"),
        "",
        "[HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize]",
        f'"AppsUseLightTheme"=dword:{light_dword}',
        f'"SystemUsesLightTheme"=dword:{light_dword}',
        "",
        "[HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\DWM]",
        f'"AccentColor"=dword:ff{_bgr_dword(theme.accent)}',
        '"ColorPrevalence"=dword:00000001',
        "",
    ]
    return "\n".join(lines) + "\n"


def render(theme: Theme) -> Mapping[str, str]:
    """``themes/<slug>/`` holding the ``.theme`` and the two ``.reg`` files."""
    return {
        f"themes/{theme.slug}/{theme.slug}.theme": _render_theme_file(theme),
        f"themes/{theme.slug}/{theme.slug}-console.reg": _render_console_reg(theme),
        f"themes/{theme.slug}/{theme.slug}-accent.reg": _render_accent_reg(theme),
    }


TARGET = Target(
    id="windows",
    target_dir="Desktops/Windows",
    render=render,
    supports_mono=False,
    legacy_files=(
        "Spacecraft-Software.theme",
        "Spacecraft_Software_CMD.reg",
        "Spacecraft_Software_dark.reg",
    ),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-windows.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-windows-theme.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Windows desktop theme (.theme) plus console and accent colour (.reg)",
)
