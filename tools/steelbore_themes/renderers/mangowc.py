# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""MangoWC desktop theme — a tiling window manager configuration.

Renders one TOML per theme, mapping MangoWC's [Colors] keys onto §11.1 roles:
bg_color → background, fg_color → foreground, active_border → accent,
inactive_border → structure, button_bg → surface, button_fg → foreground.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.toml`` per theme."""
    lines = [theme.header("MangoWC desktop theme").rstrip("\n"), ""]
    lines += [
        "[Theme]",
        f'name = "{theme.name}"',
        "",
        "[Colors]",
        f'bg_color = "{theme.background}"',
        f'fg_color = "{theme.foreground}"',
        "",
        f'active_border = "{theme.accent}"',
        f'inactive_border = "{theme.structure}"',
        "",
        f'button_bg = "{theme.surface}"',
        f'button_fg = "{theme.foreground}"',
        "",
        "[Window]",
        "border_width = 2",
        "border_radius = 4",
        "",
        "[Gaps]",
        "inner = 5",
        "outer = 10",
        "",
    ]
    return {f"themes/{theme.slug}.toml": "\n".join(lines)}


TARGET = Target(
    id="mangowc",
    target_dir="Desktops/MangoWC",
    render=render,
    supports_mono=False,
    legacy_files=("theme.toml",),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-mangowc.zip",
            fmt="zip",
            entries=(
                ("themes", "themes"),
                ("INSTALL.md", "INSTALL.md"),
                ("Spacecraft_Software_wallpaper_blue.png", "wallpaper.png"),
                ("icon.png", "icon.png"),
            ),
        ),
        Archive(
            path="Desktops/spacecraft-software-mangowc-theme.tar.gz",
            fmt="tar.gz",
            entries=(
                ("themes", "themes"),
                ("INSTALL.md", "INSTALL.md"),
                ("Spacecraft_Software_wallpaper_blue.png", "wallpaper.png"),
                ("icon.png", "icon.png"),
            ),
        ),
    ),
    description="MangoWC tiling window manager themes (TOML configuration)",
)
