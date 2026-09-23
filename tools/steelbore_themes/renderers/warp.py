# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Warp terminal — YAML theme renderer.

Generates themes in Warp's native YAML format with role-mapped colors from
the theme palette. Supports all 24 hex themes; mono is not supported by this
format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.yaml`` per theme."""
    # Start with header comment lines
    lines = [theme.header("Warp terminal theme").rstrip("\n"), ""]

    # Theme metadata and basic colors
    lines += [
        f"name: '{theme.name}'",
        f"accent: '{theme.accent}'",
        f"cursor: '{theme.focus}'",
        f"background: '{theme.background}'",
        f"foreground: '{theme.foreground}'",
        f"details: {'lighter' if theme.is_light else 'darker'}",
        "terminal_colors:",
        "  normal:",
    ]

    # Normal ANSI colors (0-7)
    for slot in ANSI_SLOTS:
        lines.append(f"    {slot}: '{theme.ansi[slot]}'")

    lines += ["  bright:"]

    # Bright ANSI colors (8-15)
    for slot in ANSI_SLOTS:
        lines.append(f"    {slot}: '{theme.ansi_bright[slot]}'")

    lines.append("")

    return {f"themes/{theme.slug}.yaml": "\n".join(lines)}


TARGET = Target(
    id="warp",
    target_dir="Terminals/Warp",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.yaml",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-warp.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Warp terminal colour themes (include themes/<slug>.yaml)",
)
