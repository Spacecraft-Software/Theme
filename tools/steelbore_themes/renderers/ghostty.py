# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Ghostty terminal — renderer for the Spacecraft Software theme family.

Renders every theme into Ghostty's native configuration format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>`` per theme (Ghostty theme files are extensionless)."""
    lines = [theme.header("Ghostty terminal theme").rstrip("\n"), ""]

    # Canvas and text
    lines += [
        f"background = {theme.background}",
        f"foreground = {theme.foreground}",
    ]

    # Cursor: cursor-color is the cursor body, cursor-text is text on cursor
    lines += [
        f"cursor-color = {theme.focus}",
        f"cursor-text = {theme.background}",
    ]

    # Selection: the canvas/foreground swap keeps both legible on every
    # palette (a solid text_safe_accent fill with background text on top is
    # the only verified inversion — see kitty.py / rio.py / alacritty.py /
    # wezterm.py for the same pattern).
    lines += [
        f"selection-background = {theme.text_safe_accent}",
        f"selection-foreground = {theme.background}",
        "",
    ]

    # ANSI colors 0-7
    for index, slot in enumerate(ANSI_SLOTS):
        lines.append(f"palette = {index}={theme.ansi[slot]}")

    lines.append("")

    # ANSI bright colors 8-15
    for index, slot in enumerate(ANSI_SLOTS, start=8):
        lines.append(f"palette = {index}={theme.ansi_bright[slot]}")

    lines.append("")
    return {f"themes/{theme.slug}": "\n".join(lines)}


TARGET = Target(
    id="ghostty",
    target_dir="Terminals/Ghostty",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-ghostty.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Ghostty terminal colour themes (include themes/<slug> files)",
)
