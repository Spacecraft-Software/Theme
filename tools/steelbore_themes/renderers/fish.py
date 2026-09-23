# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Fish shell — syntax-highlighting and prompt renderer.

Emits one ``themes/<slug>.fish`` snippet per theme: every ``fish_color_*``
and ``fish_pager_color_*`` universal variable the legacy hand-written file
set (plus ``fish_color_cancel`` and ``fish_color_valid_path``, which it did
not), and the ``fish_prompt`` function.

Fish's ``fish_color_*`` variables take either a bare ``RRGGBB`` hex (no
``#``) or one of fish's own colour names (``normal``, ``red``, ``brwhite``,
...). :attr:`Theme.is_mono` selects between the two: hex themes emit
``theme.hex_bare``-style bare hex, ``steelbore-mono`` emits fish colour
names translated from its ANSI role names (``theme.roles`` holds
``"default"``, ``"blue"``, ``"bright-white"``, ``"reverse-video"``, ... for
that theme; fish has no bare "default" or "reverse-video" colour name, so
those map to ``normal`` plus, for ``reverse-video``, a trailing
``--reverse`` attribute). The validator only checks for literal
``#RRGGBB`` text, so it cannot see these bare hexes; they are audited by
reading the rendered output instead (tools/README.md rule 1).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from steelbore_themes.core import Theme

_BRIGHT_PREFIX = "bright-"


def _mono_token(ansi_name: str) -> str:
    """A Steelbore Mono role value → the closest fish colour-name token.

    Fish has no ``default`` or ``reverse-video`` colour name: ``default``
    (no hue asserted) and ``reverse-video`` (an attribute, not a hue) both
    resolve to ``normal`` here; ``reverse-video``'s inversion is restored by
    the caller as a separate ``--reverse`` attribute. ``bright-*`` becomes
    fish's ``br*`` prefix (``bright-white`` → ``brwhite``); the eight plain
    ANSI names (``black``, ``red``, ... ``white``) are fish colour names
    already and pass through unchanged.
    """
    if ansi_name in ("default", "reverse-video"):
        return "normal"
    if ansi_name.startswith(_BRIGHT_PREFIX):
        return "br" + ansi_name.removeprefix(_BRIGHT_PREFIX)
    return ansi_name


def _fish_colour(theme: Theme, hex_value: str) -> str:
    """``hex_value`` (a ``#RRGGBB`` role hex, or a mono ANSI role name) as the
    fish colour token for that theme: bare hex for a hex theme, a fish colour
    name for mono."""
    if theme.is_mono:
        return _mono_token(hex_value)
    return hex_value.lstrip("#")


def _set_line(name: str, theme: Theme, hex_value: str, *, extra_attrs: Sequence[str] = ()) -> str:
    """``set -g <name> <colour> [attrs...]`` for one ``fish_color_*`` variable."""
    token = _fish_colour(theme, hex_value)
    attrs = list(extra_attrs)
    if theme.is_mono and hex_value == "reverse-video":
        attrs = ["--reverse", *attrs]
    value = " ".join([token, *attrs]) if attrs else token
    return f"set -g {name} {value}"


def _set_background_line(name: str, theme: Theme, hex_value: str) -> str:
    """``set -g <name> --background=<colour>`` (selection / search-match fills)."""
    return f"set -g {name} --background={_fish_colour(theme, hex_value)}"


def _prompt_lines(theme: Theme) -> list[str]:
    dir_colour = _fish_colour(theme, theme.structure)
    branch_colour = _fish_colour(theme, theme.text_safe_accent)
    ok_colour = _fish_colour(theme, theme.success)
    err_colour = _fish_colour(theme, theme.error)
    return [
        "# The prompt function",
        "function fish_prompt",
        "    set -l last_status $status",
        "",
        "    # Working directory",
        f"    set_color {dir_colour}",
        "    printf '%s' (prompt_pwd)",
        "    set_color normal",
        "",
        "    # Git branch, if any",
        "    if type -q git",
        "        set -l branch (git branch --show-current 2>/dev/null)",
        '        if test -n "$branch"',
        f"            set_color {branch_colour}",
        "            printf ' on  %s' $branch",
        "            set_color normal",
        "        end",
        "    end",
        "",
        "    # Status symbol",
        "    if test $last_status -eq 0",
        f"        set_color {ok_colour}",
        "    else",
        f"        set_color {err_colour}",
        "    end",
        "    printf ' ❯ '",
        "    set_color normal",
        "end",
        "",
    ]


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.fish`` snippet per theme."""
    lines = [theme.header("Fish shell theme").rstrip("\n"), ""]
    lines += [
        "# Syntax-highlighting colours",
        _set_line("fish_color_normal", theme, theme.foreground),
        _set_line("fish_color_command", theme, theme.success),
        _set_line("fish_color_keyword", theme, theme.text_safe_accent),
        _set_line("fish_color_quote", theme, theme.foreground),
        _set_line("fish_color_redirection", theme, theme.focus),
        _set_line("fish_color_end", theme, theme.structure),
        _set_line("fish_color_error", theme, theme.error),
        _set_line("fish_color_param", theme, theme.structure),
        _set_line("fish_color_comment", theme, theme.structure),
        _set_background_line("fish_color_selection", theme, theme.surface),
        _set_background_line("fish_color_search_match", theme, theme.surface),
        _set_line("fish_color_operator", theme, theme.success),
        _set_line("fish_color_escape", theme, theme.focus),
        _set_line("fish_color_autosuggestion", theme, theme.structure),
        _set_line("fish_color_cancel", theme, theme.error),
        _set_line(
            "fish_color_valid_path",
            theme,
            theme.structure,
            extra_attrs=("--underline",),
        ),
        "",
        "# Tab-completion pager colours",
        _set_line("fish_pager_color_prefix", theme, theme.focus),
        _set_line("fish_pager_color_completion", theme, theme.foreground),
        _set_line("fish_pager_color_description", theme, theme.structure),
        _set_line("fish_pager_color_progress", theme, theme.success),
        "",
    ]
    lines += _prompt_lines(theme)
    return {f"themes/{theme.slug}.fish": "\n".join(lines)}


TARGET = Target(
    id="fish",
    target_dir="Shells/Fish",
    render=render,
    supports_mono=True,
    legacy_files=("config.fish",),
    description="Fish shell colours and prompt (themes/<slug>.fish, SPACECRAFT_THEME-selectable)",
)
