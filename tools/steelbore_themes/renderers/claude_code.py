# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Claude Code CLI — settings fragment and terminal colour scheme.

Two files per hex theme under ``themes/<slug>/``:

* ``settings.json`` — a Claude Code settings fragment (``statusLine`` +
  ``theme``) meant to be merged into the user's own
  ``~/.claude/settings.json``, never copied wholesale. The status line's
  ``jq`` filter paints the model name in ``accent`` and the context-window
  percentage in ``structure`` using truecolor SGR escapes.
* ``terminal.json`` — a Windows-Terminal-style colour scheme (the format the
  legacy file used) for the terminal Claude Code itself runs in.

``steelbore-mono`` has no hex palette, so it renders ``settings.json`` only:
the status line falls back to 4-bit SGR codes derived from the theme's ANSI
role names (``theme.accent`` / ``theme.structure``), and no ``terminal.json``
is emitted.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme, hex_to_rgb
from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

# A literal backslash followed by the text "u001b" / "(" -- *not* the escape
# bytes themselves. jq's own string-literal parser is what turns "\u001b"
# into the ESC control byte and "\(" into an interpolation, at run time; the
# JSON file just needs to carry those two literal characters, which
# json.dumps produces by doubling the single backslash built here.
_JQ_ESC: str = "\\u001b"
_JQ_INTERP: str = "\\("


def _mono_sgr(ansi_name: str) -> str:
    """4-bit SGR parameter for a mono-theme ANSI role name.

    ``theme.roles[...]`` on ``steelbore-mono`` holds names like
    ``"bright-white"``, ``"blue"`` or ``"reverse-video"`` (never a hex); this
    maps each onto the matching standard SGR code (``30`` + slot index, or
    ``90`` + slot index with bold for the bright siblings).
    """
    if ansi_name == "reverse-video":
        return "7"
    if ansi_name not in ANSI_SLOTS and not ansi_name.startswith("bright-"):
        return "39"  # default foreground
    bright = ansi_name.startswith("bright-")
    base = ansi_name.removeprefix("bright-")
    if base not in ANSI_SLOTS:
        return "39"
    index = ANSI_SLOTS.index(base)
    return f"1;9{index}" if bright else f"3{index}"


def _status_line_command(accent_sgr: str, structure_sgr: str) -> str:
    """The ``jq`` one-liner painting model name (accent) and context % (structure)."""
    return (
        "jq -r '\""
        f"{_JQ_ESC}[{accent_sgr}m[{_JQ_INTERP}.model.display_name)]{_JQ_ESC}[0m "
        f"{_JQ_ESC}[{structure_sgr}m{_JQ_INTERP}.context_window.used_percentage "
        f"// 0)% context{_JQ_ESC}[0m"
        "\"'"
    )


def _settings_json(theme: Theme) -> str:
    if theme.is_mono:
        accent_sgr = _mono_sgr(theme.accent)
        structure_sgr = _mono_sgr(theme.structure)
    else:
        # Model-name label is normal-size terminal text, so restricted
        # accents (e.g. Steelbore Blue's Electric Blue, 3-4.5:1) fall back
        # to structure here -- the same rule ``theme.ansi["magenta"]``
        # already applies for ``terminal.json``.
        ar, ag, ab = hex_to_rgb(theme.text_safe_accent)
        sr, sg, sb = theme.rgb("structure")
        accent_sgr = f"38;2;{ar};{ag};{ab}"
        structure_sgr = f"38;2;{sr};{sg};{sb}"
    settings = {
        "statusLine": {
            "type": "command",
            "command": _status_line_command(accent_sgr, structure_sgr),
            "padding": 1,
        },
        "theme": "light" if theme.is_light else "dark",
    }
    # Pure JSON: no provenance header (REUSE coverage comes from REUSE.toml).
    return json.dumps(settings, indent=2) + "\n"


def _terminal_json(theme: Theme) -> str:
    scheme: dict[str, str] = {
        "name": theme.name,
        "background": theme.background,
        "foreground": theme.foreground,
        "cursorColor": theme.focus,
        "selectionBackground": theme.with_alpha("accent", "40"),
        "black": theme.ansi["black"],
        "red": theme.ansi["red"],
        "green": theme.ansi["green"],
        "yellow": theme.ansi["yellow"],
        "blue": theme.ansi["blue"],
        "purple": theme.ansi["magenta"],
        "cyan": theme.ansi["cyan"],
        "white": theme.ansi["white"],
        "brightBlack": theme.ansi_bright["black"],
        "brightRed": theme.ansi_bright["red"],
        "brightGreen": theme.ansi_bright["green"],
        "brightYellow": theme.ansi_bright["yellow"],
        "brightBlue": theme.ansi_bright["blue"],
        "brightPurple": theme.ansi_bright["magenta"],
        "brightCyan": theme.ansi_bright["cyan"],
        "brightWhite": theme.ansi_bright["white"],
    }
    return json.dumps(scheme, indent=2) + "\n"


def render(theme: Theme) -> Mapping[str, str]:
    """``themes/<slug>/settings.json`` (+ ``terminal.json`` for hex themes)."""
    files: dict[str, str] = {f"themes/{theme.slug}/settings.json": _settings_json(theme)}
    if not theme.is_mono:
        files[f"themes/{theme.slug}/terminal.json"] = _terminal_json(theme)
    return files


TARGET = Target(
    id="claude_code",
    target_dir="CLIs/Claude_Code",
    render=render,
    supports_mono=True,
    legacy_files=("settings.json", "spacecraft-software-terminal.json"),
    description=(
        "Claude Code settings fragment (statusLine + theme) and a Windows-Terminal-style colour scheme per theme"
    ),
)
