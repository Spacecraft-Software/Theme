# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Hyprland window manager — desktop theme renderer.

Renders themes in Hyprland's native configuration format. Colour roles map
to Hyprland's border, shadow, and group configuration keys.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.conf`` per theme."""
    lines = [
        theme.header("Hyprland window manager theme").rstrip("\n"),
        "",
        "general {",
        "    gaps_in = 5",
        "    gaps_out = 10",
        "    border_size = 2",
        f"    col.active_border = rgb({theme.hex_bare('accent')}) rgb({theme.hex_bare('focus')}) 45deg",
        f"    col.inactive_border = rgb({theme.hex_bare('border')})",
        "    layout = dwindle",
        "}",
        "",
        "decoration {",
        "    rounding = 4",
        "    ",
        "    blur {",
        "        enabled = true",
        "        size = 3",
        "        passes = 1",
        "    }",
        "",
        "    drop_shadow = yes",
        "    shadow_range = 4",
        "    shadow_render_power = 3",
        f"    col.shadow = rgba({theme.hex_bare('background')}ee)",
        "}",
        "",
        "group {",
        f"    col.border_active = rgb({theme.hex_bare('accent')})",
        f"    col.border_inactive = rgb({theme.hex_bare('border')})",
        "    groupbar {",
        f"        col.text = rgb({theme.hex_bare('foreground')})",
        "    }",
        "}",
        "",
        "misc {",
        f"    background_color = rgb({theme.hex_bare('background')})",
        "    disable_hyprland_logo = true",
        "    disable_splash_rendering = true",
        "}",
    ]
    return {f"themes/{theme.slug}.conf": "\n".join(lines) + "\n"}


TARGET = Target(
    id="hyprland",
    target_dir="Desktops/Hyprland",
    render=render,
    supports_mono=False,
    legacy_files=("hyprland.conf",),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-hyprland.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-hyprland-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Hyprland window manager colour themes (include themes/<slug>.conf)",
)
