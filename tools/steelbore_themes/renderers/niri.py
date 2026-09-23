# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Niri window manager — theme renderer.

Niri is a tiling Wayland compositor with support for per-theme configuration
through KDL (KDL Document Language) files. The theme controls the focus ring
gradient, border colours, and window opacity settings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.kdl`` per theme."""
    lines = [theme.header("Niri window manager theme", comment="//").rstrip("\n"), ""]
    lines += [
        "layout {",
        "    // Structural Gaps",
        "    gaps 16",
        "    ",
        "    // The Focus Ring: The primary indicator of the active window",
        "    focus-ring {",
        "        width 4",
        "        ",
        "        // Active: Gradient from accent to focus",
        f'        active-gradient from="{theme.accent}" to="{theme.focus}" angle=45',
        "        ",
        "        // Inactive: Recedes into surface",
        f'        inactive-color "{theme.surface}"',
        "    }",
        "    ",
        "    // Inner Border: Subtle definition for all windows",
        "    border {",
        "        width 1",
        f'        active-color "{theme.border}"',
        f'        inactive-color "{theme.background}"',
        "    }",
        "}",
        "",
        "// Window Rules for transparency/opacity",
        "window-rule {",
        "    // Make terminals slightly transparent to show the wallpaper",
        '    match app-id="^alacritty$"',
        '    match app-id="^org.gnome.Terminal$"',
        '    match app-id="^kitty$"',
        "    ",
        "    opacity 0.95",
        "}",
        "",
    ]
    return {f"themes/{theme.slug}.kdl": "\n".join(lines)}


TARGET = Target(
    id="niri",
    target_dir="Desktops/Niri",
    render=render,
    supports_mono=False,
    legacy_files=("config.kdl",),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-niri.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-niri-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Niri window manager KDL themes (include themes/<slug>.kdl)",
)
