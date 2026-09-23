# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Konsole terminal (KDE) - theme renderer.

Renders Steelbore palette themes into KDE Konsole .colorscheme INI format.
Konsole stores terminal appearance (background, foreground, ANSI colors) as
named sections with decimal RGB triplets.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme, hex_to_rgb
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.colorscheme`` per theme."""
    lines = [theme.header("Konsole terminal theme", comment="#").rstrip("\n"), ""]

    # General section with theme metadata
    lines += [
        "[General]",
        f"Description={theme.name}",
        "Opacity=1",
        "Wallpaper=",
        "",
    ]

    # Background colors: canvas and elevated surfaces
    bg_r, bg_g, bg_b = theme.rgb("background")
    surf_r, surf_g, surf_b = theme.rgb("surface")
    surf_alt_r, surf_alt_g, surf_alt_b = theme.rgb("surface-alt")

    lines += [
        "[Background]",
        f"Color={bg_r},{bg_g},{bg_b}",
        "",
        "[BackgroundIntense]",
        f"Color={surf_r},{surf_g},{surf_b}",
        "",
        "[BackgroundFaint]",
        f"Color={surf_alt_r},{surf_alt_g},{surf_alt_b}",
        "",
    ]

    # Foreground colors: text
    fg_r, fg_g, fg_b = theme.rgb("foreground")
    struct_r, struct_g, struct_b = theme.rgb("structure")

    lines += [
        "[Foreground]",
        f"Color={fg_r},{fg_g},{fg_b}",
        "",
        "[ForegroundIntense]",
        f"Color={fg_r},{fg_g},{fg_b}",
        "",
        "[ForegroundFaint]",
        f"Color={struct_r},{struct_g},{struct_b}",
        "",
    ]

    # ANSI colors 0-7
    lines.append("# ANSI colors (0-7)")
    for index, slot in enumerate(ANSI_SLOTS):
        r, g, b = hex_to_rgb(theme.ansi[slot])
        lines.append(f"[Color{index}]")
        lines.append(f"Color={r},{g},{b}")
        lines.append("")

    # ANSI bright colors (8-15)
    lines.append("# ANSI bright colors (8-15)")
    for index, slot in enumerate(ANSI_SLOTS):
        r, g, b = hex_to_rgb(theme.ansi_bright[slot])
        lines.append(f"[Color{index}Intense]")
        lines.append(f"Color={r},{g},{b}")
        lines.append("")

    # Faint variants (same as normal per KDE convention)
    lines.append("# ANSI faint colors (same as normal)")
    for index, slot in enumerate(ANSI_SLOTS):
        r, g, b = hex_to_rgb(theme.ansi[slot])
        lines.append(f"[Color{index}Faint]")
        lines.append(f"Color={r},{g},{b}")
        lines.append("")

    return {f"themes/{theme.slug}.colorscheme": "\n".join(lines)}


TARGET = Target(
    id="konsole",
    target_dir="Terminals/Konsole",
    render=render,
    supports_mono=False,
    legacy_files=("Spacecraft-Software.colorscheme",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-konsole.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Konsole terminal colour themes (include themes/<slug>.colorscheme)",
)
