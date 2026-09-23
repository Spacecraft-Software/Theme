# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Ion shell — prompt module theme renderer.

Generates Ion shell configuration snippets that set prompt variables by role
and render a PROMPT function using truecolor (${c::0x<hex>}) or ANSI names
(${c::color-name}) for mono.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.ion`` per theme."""
    lines: list[str] = [
        theme.header("Ion shell prompt theme").rstrip("\n"),
        "# Add to ~/.config/ion/initrc or source this file",
        "",
    ]

    if theme.is_mono:
        # Mono variant: ANSI colour names
        lines += [
            "# Colour variables (ANSI names for 4-bit mode)",
            "let background = default",
            f"let foreground = {theme.foreground}",
            f"let accent = {theme.accent}",
            f"let structure = {theme.structure}",
            f"let success = {theme.success}",
            f"let error = {theme.error}",
            f"let warning = {theme.warning}",
            f"let focus = {theme.focus}",
            "",
            "# Prompt function using ANSI colour names",
        ]
    else:
        # Hex variant: truecolor hex codes
        lines += [
            "# Colour variables (bare hex for truecolor)",
            f"let background = {theme.hex_bare('background')}",
            f"let foreground = {theme.hex_bare('foreground')}",
            f"let accent = {theme.hex_bare('accent')}",
            f"let structure = {theme.hex_bare('structure')}",
            f"let success = {theme.hex_bare('success')}",
            f"let error = {theme.hex_bare('error')}",
            f"let warning = {theme.hex_bare('warning')}",
            f"let focus = {theme.hex_bare('focus')}",
            "",
            "# Prompt function using truecolor hex codes",
        ]

    if theme.is_mono:
        prompt_lines = [
            "fn PROMPT",
            '    let dir = "${c::' + theme.structure + '}${PWD}${c::reset}"',
            '    let symbol = "❯"',
            "    ",
            "    if eq $? 0",
            '        print "${dir} ${c::' + theme.success + '}${symbol}${c::reset} "',
            "    else",
            '        print "${dir} ${c::' + theme.error + '}${symbol}${c::reset} "',
            "    end",
            "end",
        ]
    else:
        prompt_lines = [
            "fn PROMPT",
            '    let dir = "${c::0x${structure}}${PWD}${c::reset}"',
            '    let symbol = "❯"',
            "    ",
            "    if eq $? 0",
            '        print "${dir} ${c::0x${success}}${symbol}${c::reset} "',
            "    else",
            '        print "${dir} ${c::0x${error}}${symbol}${c::reset} "',
            "    end",
            "end",
        ]

    lines.extend(prompt_lines)
    lines.append("")

    return {f"themes/{theme.slug}.ion": "\n".join(lines)}


TARGET = Target(
    id="ion",
    target_dir="Shells/Ion",
    render=render,
    supports_mono=True,
    legacy_files=("initrc",),
    description="Ion shell prompt theme modules (include themes/<slug>.ion in ~/.config/ion/initrc)",
)
