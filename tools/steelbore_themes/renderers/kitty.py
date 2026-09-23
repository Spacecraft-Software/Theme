# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Kitty terminal — reference renderer.

This is the template every other renderer follows: a pure function from
:class:`Theme` to text, every colour read through a role accessor, a
provenance header, and a :data:`TARGET` describing where the output lives.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.conf`` per theme."""
    lines = [theme.header("Kitty terminal theme").rstrip("\n"), ""]
    # Cursor and selection: the canvas/foreground swap keeps both legible on
    # every palette (foreground on background is the palette's best pair).
    lines += [
        f"foreground           {theme.foreground}",
        f"background           {theme.background}",
        f"selection_foreground {theme.background}",
        f"selection_background {theme.text_safe_accent}",
        f"cursor               {theme.foreground}",
        f"cursor_text_color    {theme.background}",
        f"url_color            {theme.structure}",
        "",
        "# Normal colors",
    ]
    for index, slot in enumerate(ANSI_SLOTS):
        lines.append(f"color{index}  {theme.ansi[slot]}")
    lines += ["", "# Bright colors"]
    for index, slot in enumerate(ANSI_SLOTS, start=8):
        lines.append(f"color{index} {theme.ansi_bright[slot]}")
    lines += [
        "",
        "# Tab bar — surface fills carry no text of their own (§11.0.1); the",
        "# tab text is the foreground on the surface, a verified pairing.",
        f"active_tab_foreground   {theme.background}",
        f"active_tab_background   {theme.text_safe_accent}",
        f"inactive_tab_foreground {theme.foreground}",
        f"inactive_tab_background {theme.surface}",
        f"tab_bar_background      {theme.surface_alt}",
        "",
        "# Marks / borders",
        f"active_border_color   {theme.focus}",
        f"inactive_border_color {theme.border}",
        f"bell_border_color     {theme.warning}",
        "",
    ]
    return {f"themes/{theme.slug}.conf": "\n".join(lines)}


TARGET = Target(
    id="kitty",
    target_dir="Terminals/Kitty",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.conf",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-kitty.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Kitty terminal colour themes (include themes/<slug>.conf)",
)
