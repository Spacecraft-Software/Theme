# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""XFCE Terminal — colour scheme INI renderer.

Renders Steelbore palette themes into XFCE Terminal's .theme colour scheme
INI format. XFCE Terminal reads schemes from
``~/.local/share/xfce4/terminal/colorschemes/`` and selects them via the
Preferences dialog.

The format stores terminal appearance as section ``[Scheme]`` with keys for
background, foreground, cursor, selection, tab activity, and 16 ANSI colours
in a single semicolon-separated ``ColorPalette`` line.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.theme`` per theme."""
    lines = [theme.header("XFCE Terminal colour scheme").rstrip("\n"), ""]

    lines += [
        "[Scheme]",
        f"Name={theme.name}",
        f"ColorBackground={theme.background}",
        f"ColorForeground={theme.foreground}",
        f"ColorCursor={theme.focus}",
        "ColorCursorUseDefault=FALSE",
        f"ColorSelection={theme.background}",
        "ColorSelectionUseDefault=FALSE",
        f"ColorSelectionBackground={theme.accent}",
        f"ColorBold={theme.foreground}",
        "ColorBoldUseDefault=FALSE",
        f"TabActivityColor={theme.warning}",
        f"ColorPalette={';'.join(theme.ansi16())}",
    ]

    return {f"themes/{theme.slug}.theme": "\n".join(lines) + "\n"}


TARGET = Target(
    id="xfce_terminal",
    target_dir="Terminals/XFCE_Terminal",
    render=render,
    supports_mono=False,
    legacy_files=("Spacecraft-Software.theme", "terminalrc"),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-xfce_terminal.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="XFCE Terminal colour schemes (themes/<slug>.theme)",
)
