# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Bash prompt module — reproduces the legacy ``spacecraft_software_prompt``.

Emits one ``themes/<slug>.sh`` per theme: a function that colours ``PS1``
from this theme's ``structure`` / ``accent`` / ``success`` / ``error`` roles
(§11.1) and installs itself via ``PROMPT_COMMAND``. The file is meant to be
*sourced* from ``~/.bashrc``, never executed, so it carries no shebang.

Hex themes get 24-bit truecolor SGR (``\\[\\e[38;2;R;G;Bm\\]``) built from
``theme.rgb``. ``steelbore-mono`` carries no hex palette (§11.1.1) — its
roles resolve to ANSI colour *names* (``"blue"``, ``"bright-white"``, ...)
instead, so the mono branch looks those up in the conventional 4-bit SGR
table below and emits plain ``\\[\\e[<code>m\\]`` sequences. That table is a
routing of ANSI *names* to their standard SGR numbers, not a colour value of
its own, so it carries no hex literal either way.

The module stays prompt-only: no ``LS_COLORS`` export, nothing else sourced.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from steelbore_themes.core import Theme, hex_to_rgb
from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

_RESET: Final[str] = "\\[\\e[0m\\]"

_MONO_SGR: Final[Mapping[str, str]] = {
    "default": "39",
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
    "reverse-video": "7",
}
"""Conventional 4-bit SGR codes for the ANSI names ``steelbore-mono`` roles
resolve to (``core.py``'s ``[themes.steelbore-mono]`` table)."""


def _sgr_true(value: str) -> str:
    """``\\[\\e[38;2;R;G;Bm\\]`` — truecolor foreground from a role's hex."""
    r, g, b = hex_to_rgb(value)
    return f"\\[\\e[38;2;{r};{g};{b}m\\]"


def _sgr_mono(name: str) -> str:
    """``\\[\\e[<code>m\\]`` — 4-bit foreground from a role's ANSI name."""
    code = _MONO_SGR.get(name, _MONO_SGR["default"])
    return f"\\[\\e[{code}m\\]"


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.sh`` Bash prompt module per theme."""
    header = theme.header("Bash prompt theme").rstrip("\n")

    if theme.is_mono:
        c_dir = _sgr_mono(theme.structure)
        c_git = _sgr_mono(theme.text_safe_accent)
        c_success = _sgr_mono(theme.success)
        c_fail = _sgr_mono(theme.error)
    else:
        c_dir = _sgr_true(theme.structure)
        c_git = _sgr_true(theme.text_safe_accent)
        c_success = _sgr_true(theme.success)
        c_fail = _sgr_true(theme.error)

    lines = [
        header,
        "",
        "# Sourced from ~/.bashrc -- not executed directly, so no shebang.",
        "# Installs a PROMPT_COMMAND that colours PS1 from this theme's",
        "# structure / accent / success / error roles (Steelbore Standard",
        "# Sec. 11.1). Prompt-only: no LS_COLORS export, nothing else sourced.",
        "",
        "spacecraft_software_prompt() {",
        "    local EXIT_CODE=$?",
        "",
        f'    local C_RESET="{_RESET}"',
        f'    local C_DIR="{c_dir}"',
        f'    local C_GIT="{c_git}"',
        f'    local C_SUCCESS="{c_success}"',
        f'    local C_FAIL="{c_fail}"',
        "",
        '    local GIT_BRANCH=""',
        "    if git rev-parse --is-inside-work-tree &>/dev/null; then",
        "        GIT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || git describe --tags --always 2>/dev/null)",
        '        GIT_BRANCH=" ${C_GIT}on  ${GIT_BRANCH}"',
        "    fi",
        "",
        '    local STATUS_SYMBOL="❯"',
        "    local STATUS_COLOR=$C_SUCCESS",
        "    if [ $EXIT_CODE -ne 0 ]; then",
        "        STATUS_COLOR=$C_FAIL",
        "    fi",
        "",
        '    PS1="${C_DIR}\\w${GIT_BRANCH} ${STATUS_COLOR}${STATUS_SYMBOL} ${C_RESET}"',
        "}",
        "",
        "PROMPT_COMMAND=spacecraft_software_prompt",
        "",
    ]
    return {f"themes/{theme.slug}.sh": "\n".join(lines)}


TARGET = Target(
    id="bash",
    target_dir="Shells/Bash",
    render=render,
    supports_mono=True,
    legacy_files=(".bash_profile",),
    description="Bash prompt modules (source themes/<slug>.sh from ~/.bashrc)",
)
