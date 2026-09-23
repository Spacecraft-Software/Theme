# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Zsh prompt -- role-driven reproduction of the legacy Spacecraft Software prompt.

Reproduces the hand-written ``.zshrc`` prompt module -- a ``vcs_info``-styled
branch readout, a directory + status-glyph left prompt, and a dim right-hand
clock -- then extends it with a couple of genuinely useful, standard zsh
prompt idioms (a staged/unstaged VCS indicator and a vi-mode command
indicator) so the generated theme exercises more of the eight-slot ANSI role
set than the legacy file did.

Every colour comes from :attr:`Theme.ansi`, which already resolves to the
right shape for both variants: a ``#RRGGBB`` hex for a colour theme (Zsh's
``%F{#RRGGBB}`` 24-bit syntax) and a bare 4-bit ANSI colour name for
``steelbore-mono`` (Zsh's ``%F{blue}`` name syntax) -- so one format string
is correct for both. ``theme.ansi`` is used instead of role accessors
directly because it is the one mapping guaranteed to hold Zsh-valid colour
*names* in mono mode (``blue``, ``green``, ``red``, ``yellow``, ``magenta``,
``cyan``, ``white``); the bare role table holds mono values such as
``"bright-white"`` and ``"reverse-video"`` that Zsh's ``%F{}`` does not
understand.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.zsh`` prompt module per theme."""
    structure = theme.ansi["blue"]
    accent = theme.ansi["magenta"]  # text-safe: derived from text_safe_accent
    success = theme.ansi["green"]
    error = theme.ansi["red"]
    warning = theme.ansi["yellow"]
    focus = theme.ansi["cyan"]
    foreground = theme.ansi["white"]
    polarity = "light" if theme.is_light else "dark"

    lines = [
        theme.header("Zsh prompt theme").rstrip("\n"),
        "",
        "# Canvas polarity (informational -- a text prompt carries no",
        "# background fill of its own, but a companion script may branch",
        "# on this instead of hardcoding light/dark).",
        f'typeset -g SPACECRAFT_THEME_POLARITY="{polarity}"',
        "",
        "autoload -Uz vcs_info",
        "precmd() { vcs_info }",
        "",
        "# VCS branch readout -- accent, text-safe on every palette --",
        "# plus a staged/unstaged dirty indicator (success/warning).",
        f"zstyle ':vcs_info:*' formats ' %F{{{accent}}}on  %b%c%u%f'",
        f"zstyle ':vcs_info:*' actionformats ' %F{{{accent}}}on  %b|%a%c%u%f'",
        "zstyle ':vcs_info:*' check-for-changes true",
        f"zstyle ':vcs_info:*' stagedstr ' %F{{{success}}}●%f'",
        f"zstyle ':vcs_info:*' unstagedstr ' %F{{{warning}}}●%f'",
        "",
        "# Vi-mode command indicator (focus) -- shown only in normal",
        "# (command) mode so insert mode stays visually quiet.",
        "function zle-keymap-select {",
        "    if [[ ${KEYMAP} == vicmd ]]; then",
        f"        VI_MODE_INDICATOR='%F{{{focus}}}■%f '",
        "    else",
        "        VI_MODE_INDICATOR=''",
        "    fi",
        "    zle reset-prompt",
        "}",
        "zle -N zle-keymap-select",
        "",
        "setopt PROMPT_SUBST",
        "",
        "# Left: vi-mode indicator, directory (structure), VCS branch,",
        "# exit-status glyph (success/error).",
        "PROMPT='${VI_MODE_INDICATOR}"
        f"%F{{{structure}}}%~${{vcs_info_msg_0_}} "
        f"%(?.%F{{{success}}}❯.%F{{{error}}}❯) %f'",
        "",
        "# Right: background-job count (foreground), clock (structure).",
        f"RPROMPT='%(1j.%F{{{foreground}}}[%j]%f .)%F{{{structure}}}%*%f'",
        "",
    ]
    return {f"themes/{theme.slug}.zsh": "\n".join(lines)}


TARGET = Target(
    id="zsh",
    target_dir="Shells/Zsh",
    render=render,
    supports_mono=True,
    legacy_files=(".zshrc",),
    description="Zsh prompt themes (source themes/<slug>.zsh from ~/.zshrc)",
)
