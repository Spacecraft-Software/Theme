# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Linux virtual console (TTY) — palette-script renderer.

Emits a POSIX ``sh`` script that sets the Linux console's 16-colour palette
via the private ``ESC ] P nc`` escape (``console_codes(4)``) when running on
an actual virtual console (``$TERM = linux``), then sets a default
foreground/background pair and clears the screen so existing glyphs repaint
with the new palette. It never touches anything inside a pseudo-terminal
(xterm, tmux, SSH, ...), matching the hand-written legacy script this
replaces.

The mono theme (``steelbore-mono``) carries no hex palette (§11.1.1): its
script only resets terminal attributes and sets no console palette entries,
so a ``NO_COLOR`` session defers all hue to whatever 16-colour palette the
console already has.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def _palette_lines(theme: Theme) -> list[str]:
    """One ``printf`` line per ANSI slot 0-15 loading a console palette entry.

    ``console_codes(4)``'s private ``ESC ] P nc`` sequence takes the slot
    index as a single hex digit (``0``-``F``) immediately followed by the
    six-digit colour with no ``#``; ``theme.ansi16()`` already carries the
    role-derived colours in slot order (§11.1 role table, black=background
    through white=foreground, bright siblings 8-15).
    """
    lines: list[str] = []
    for index, value in enumerate(theme.ansi16()):
        lines.append(f"    printf '\\033]P{index:X}{value.lstrip('#')}'")
    return lines


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.sh`` Linux-console palette script per theme."""
    header = theme.header("Linux console (TTY) palette script").rstrip("\n")

    if theme.is_mono:
        lines = [
            "#!/bin/sh",
            header,
            "",
            "# Steelbore Mono carries no hex palette (§11.1.1). This script",
            "# only resets terminal attributes and sets no console palette",
            "# entries -- mono mode defers every hue to whatever 16-colour",
            "# palette the Linux console (or the operator's own setup)",
            "# already carries, which is what NO_COLOR sessions expect.",
            "",
            "printf '\\033[0m'",
            "",
        ]
        return {f"themes/{theme.slug}.sh": "\n".join(lines)}

    lines = [
        "#!/bin/sh",
        header,
        "",
        "# Sets the Linux virtual console's 16-colour palette via the",
        '# private "ESC ] P nc" escape (console_codes(4)). Only takes',
        "# effect on an actual Linux console ($TERM = linux) -- a",
        "# pseudo-terminal (xterm, tmux, SSH, ...) ignores or mishandles",
        "# the escape, so this is a deliberate no-op there.",
        "",
        'if [ "$TERM" = "linux" ]; then',
        *_palette_lines(theme),
        "",
        "    # Default foreground/background: SGR 37/40 select ANSI slots 7",
        "    # (white -> foreground) and 0 (black -> background), which the",
        "    # printf lines above already loaded with this theme's colours;",
        "    # clear repaints the whole screen with them applied.",
        "    printf '\\033[37;40m'",
        "    clear",
        "fi",
        "",
    ]
    return {f"themes/{theme.slug}.sh": "\n".join(lines)}


TARGET = Target(
    id="tty",
    target_dir="Shells/TTY",
    render=render,
    supports_mono=True,
    legacy_files=("spacecraft_software_tty.sh",),
    description="Linux virtual console (TTY) palette scripts (themes/<slug>.sh)",
)
