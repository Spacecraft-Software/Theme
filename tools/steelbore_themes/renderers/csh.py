# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""C shell (csh/tcsh) — prompt theme generator.

Emits one ``themes/<slug>.csh`` per theme, meant to be sourced from
``~/.cshrc``. Reproduces the legacy ``.cshrc``'s ``red``/``green``/``blue``/
``amber``/``reset`` variable names verbatim (error / success / structure /
text-safe-accent / reset), set as truecolor or 4-bit ANSI SGR sequences, then
builds ``set prompt`` from ``blue`` (structure, cwd) and ``amber`` (text-safe
accent, prompt character) before unsetting the temporaries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import Theme, hex_to_rgb
from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def _ansi_code(name: str) -> str:
    """4-bit ANSI colour name → SGR code (e.g., 'blue' → '34')."""
    ansi_codes = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "bright-black": "90",
        "bright-red": "91",
        "bright-green": "92",
        "bright-yellow": "93",
        "bright-blue": "94",
        "bright-magenta": "95",
        "bright-cyan": "96",
        "bright-white": "97",
        "default": "39",
        "reverse-video": "7",
    }
    return ansi_codes.get(name, "39")


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.csh`` per theme (truecolor or mono).

    Sets ``red``/``green``/``blue``/``amber``/``reset`` as SGR sequences
    wrapped in ``%{ %}`` (csh prompt expansion) — the same five names the
    legacy ``.cshrc`` defined, from the error / success / structure /
    text-safe-accent roles. Only ``blue`` (structure, cwd) and ``amber``
    (text-safe accent, prompt character) drive the prompt itself, matching
    the legacy prompt line, but all five are defined for parity with anyone
    sourcing this file for the colour variables alone. Mono themes use plain
    4-bit ANSI codes instead of truecolor.
    """
    lines = [theme.header("C shell (csh/tcsh) prompt theme").rstrip("\n"), ""]

    if theme.is_mono:
        # 4-bit ANSI codes for mono themes — theme.error/.success/.structure
        # and text_safe_accent resolve to ANSI colour *names* for mono.
        red_code = _ansi_code(theme.error)
        green_code = _ansi_code(theme.success)
        blue_code = _ansi_code(theme.structure)
        amber_code = _ansi_code(theme.text_safe_accent)
        reset_code = "0"

        lines += [
            "# Mono (4-bit ANSI) — follows terminal colors; set SPACECRAFT_THEME=steelbore-mono",
            "",
            f'set   red = "%{{\\033[{red_code}m%}}"',
            f'set green = "%{{\\033[{green_code}m%}}"',
            f'set  blue = "%{{\\033[{blue_code}m%}}"',
            f'set amber = "%{{\\033[{amber_code}m%}}"',
            f'set reset = "%{{\\033[{reset_code}m%}}"',
            "",
            "# Prompt: [dir] [prompt char]",
            'set prompt = "${blue}%~ ${amber}%# ${reset}"',
            "",
            "# Clean up variables",
            "unset red green blue amber reset",
        ]
    else:
        # Truecolor SGR sequences for hex themes.
        red_rgb = theme.rgb("error")
        green_rgb = theme.rgb("success")
        blue_rgb = theme.rgb("structure")
        # text_safe_accent is a property that returns a hex string.
        amber_rgb = hex_to_rgb(theme.text_safe_accent)
        reset_seq = "0"

        lines += [
            "# Truecolor SGR sequences — set SPACECRAFT_THEME=<slug> to switch",
            "",
            f'set   red = "%{{\\033[38;2;{red_rgb[0]};{red_rgb[1]};{red_rgb[2]}m%}}"',
            f'set green = "%{{\\033[38;2;{green_rgb[0]};{green_rgb[1]};{green_rgb[2]}m%}}"',
            f'set  blue = "%{{\\033[38;2;{blue_rgb[0]};{blue_rgb[1]};{blue_rgb[2]}m%}}"',
            f'set amber = "%{{\\033[38;2;{amber_rgb[0]};{amber_rgb[1]};{amber_rgb[2]}m%}}"',
            f'set reset = "%{{\\033[{reset_seq}m%}}"',
            "",
            "# Prompt: [dir] [prompt char]",
            'set prompt = "${blue}%~ ${amber}%# ${reset}"',
            "",
            "# Clean up variables",
            "unset red green blue amber reset",
        ]

    return {f"themes/{theme.slug}.csh": "\n".join(lines) + "\n"}


TARGET = Target(
    id="csh",
    target_dir="Shells/Csh",
    render=render,
    supports_mono=True,
    legacy_files=(".cshrc",),
    description="C shell (csh/tcsh) colour prompt themes",
)
