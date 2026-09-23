# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Nushell colour-config module renderer.

Emits one ``themes/<slug>.nu`` per theme: an ``export def main [] { return
{ ... } }`` module matching the shape Nushell's ``$env.config.color_config``
expects — the legacy hand-written keys (``separator``, ``header``, ``int``,
``filesize``, ``date``, ``string``, ``bool``, ``row_index``, the
``shape_*`` syntax-highlighting table) plus the rest of the documented
``color_config`` surface (structured-value keys, ``search_result``, and the
remaining ``shape_*`` entries Nushell defines).

Every value is read through a role accessor (§11.1) and mapped onto the
closest meaning in the ``tools/README.md`` role table: numbers and
durations take ``warning`` ("numbers & constants"), function-like shapes
(``internalcall``, ``custom``, ``signature``, ``filepath``, ``directory``,
``globpattern``) take ``focus`` ("functions" plus navigable paths),
keyword-class tokens (``keyword``, ``bool``, ``match_pattern``, ``variable``,
``vardecl``) take ``accent``, string-like literals take ``success``, and
everything else structural (operators, punctuation, compound/container
types, comments-adjacent text) takes ``structure``. ``shape_garbage`` is the
one deliberate inversion: canvas text on an ``error`` fill, the same
verified pair measured the other way round (rule 3).

``steelbore-mono`` carries no hex palette (§11.1.1) — role values resolve to
ANSI-style names (``"blue"``, ``"bright-white"``, ``"reverse-video"``, ...)
instead, so :func:`_mono_name` routes those to Nushell's own colour-name
vocabulary (``red``, ``green``, ``blue``, ``purple``, ``cyan``, ``white``,
``black``, ``default``, and the ``light_*`` bright siblings). Nushell has no
dedicated "reverse video" colour name, so that token resolves to ``default``
— the one theme that uses it for a role (``focus``) only ever appears in
plain string slots here, so the reversal itself is not reproducible in
mono and is a documented, low-stakes deviation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from steelbore_themes.core import Theme

_NU_COLOR_NAMES: Final[Mapping[str, str]] = {
    "default": "default",
    "black": "black",
    "red": "red",
    "green": "green",
    "yellow": "yellow",
    "blue": "blue",
    "magenta": "purple",
    "cyan": "cyan",
    "white": "white",
}
"""ANSI slot name -> Nushell colour name (Nushell says ``purple``, not
``magenta``; every other plain slot name is already a Nushell colour name)."""


def _mono_name(ansi_value: str) -> str:
    """A Steelbore Mono role value -> the nearest Nushell colour name.

    ``default`` and ``reverse-video`` (an attribute, not a hue) both resolve
    to ``default``. ``bright-<slot>`` becomes Nushell's ``light_<slot>``
    prefix, except ``bright-white`` — Nushell has no ``light_white`` — which
    stays ``white``, the brightest plain name.
    """
    if ansi_value in ("default", "reverse-video"):
        return "default"
    if ansi_value == "bright-white":
        return "white"
    if ansi_value.startswith("bright-"):
        base = ansi_value.removeprefix("bright-")
        return f"light_{_NU_COLOR_NAMES.get(base, base)}"
    return _NU_COLOR_NAMES.get(ansi_value, ansi_value)


def _c(theme: Theme, value: str) -> str:
    """Quoted Nushell colour literal for a role's already-resolved value."""
    return f'"{_mono_name(value) if theme.is_mono else value}"'


_ROLE_GETTERS: Final[Mapping[str, Callable[[Theme], str]]] = {
    "background": lambda t: t.background,
    "surface": lambda t: t.surface,
    "foreground": lambda t: t.foreground,
    "accent": lambda t: t.text_safe_accent,
    "structure": lambda t: t.structure,
    "success": lambda t: t.success,
    "error": lambda t: t.error,
    "warning": lambda t: t.warning,
    "focus": lambda t: t.focus,
}
"""Role name -> accessor.  ``accent`` reads ``text_safe_accent`` throughout —
every use here is a text slot (rule 4)."""


def _v(theme: Theme, role: str) -> str:
    """Quoted colour literal for a named role, resolved on ``theme``."""
    return _c(theme, _ROLE_GETTERS[role](theme))


def _plain(theme: Theme, key: str, role: str) -> str:
    return f"{key}: {_v(theme, role)}"


def _bold(theme: Theme, key: str, role: str) -> str:
    return f'{key}: {{ fg: {_v(theme, role)} attr: "b" }}'


def _fill(theme: Theme, key: str, fg_role: str, bg_role: str, *, bold: bool = False) -> str:
    attr = ' attr: "b"' if bold else ""
    return f"{key}: {{ fg: {_v(theme, fg_role)} bg: {_v(theme, bg_role)}{attr} }}"


# -- the data-driven key tables ----------------------------------------------

_TOP_PLAIN: Final[tuple[tuple[str, str], ...]] = (
    ("separator", "structure"),
    ("leading_trailing_space_bg", "surface"),
    ("empty", "structure"),
    ("int", "warning"),
    ("filesize", "focus"),
    ("duration", "warning"),
    ("date", "structure"),
    ("range", "warning"),
    ("float", "warning"),
    ("string", "foreground"),
    ("nothing", "structure"),
    ("binary", "structure"),
    ("cellpath", "foreground"),
    ("record", "structure"),
    ("list", "structure"),
    ("block", "structure"),
    ("hints", "structure"),
)
"""Top-level ``color_config`` keys whose value is a single role colour."""

_TOP_BOLD: Final[tuple[tuple[str, str], ...]] = (
    ("header", "success"),
    ("row_index", "success"),
)
"""Top-level keys rendered as ``{ fg: <role> attr: "b" }``."""

_SHAPE_PLAIN: Final[tuple[tuple[str, str], ...]] = (
    ("shape_and", "structure"),
    ("shape_or", "structure"),
    ("shape_binary", "structure"),
    ("shape_block", "structure"),
    ("shape_bool", "accent"),
    ("shape_closure", "structure"),
    ("shape_custom", "focus"),
    ("shape_datetime", "structure"),
    ("shape_directory", "focus"),
    ("shape_external", "foreground"),
    ("shape_external_resolved", "success"),
    ("shape_externalarg", "foreground"),
    ("shape_filepath", "focus"),
    ("shape_flag", "structure"),
    ("shape_float", "warning"),
    ("shape_globpattern", "focus"),
    ("shape_int", "warning"),
    ("shape_internalcall", "focus"),
    ("shape_keyword", "accent"),
    ("shape_list", "structure"),
    ("shape_literal", "structure"),
    ("shape_match_pattern", "accent"),
    ("shape_matching_brackets", "focus"),
    ("shape_nothing", "structure"),
    ("shape_operator", "structure"),
    ("shape_pipe", "structure"),
    ("shape_range", "warning"),
    ("shape_record", "structure"),
    ("shape_redirection", "structure"),
    ("shape_signature", "focus"),
    ("shape_string", "success"),
    ("shape_string_interpolation", "success"),
    ("shape_table", "structure"),
    ("shape_variable", "accent"),
    ("shape_vardecl", "accent"),
    ("shape_raw_string", "success"),
)
"""``shape_*`` syntax-highlighting keys (parser-token colours), each a single
role colour. ``shape_garbage`` and ``shape_bool``'s value-based sibling
(top-level ``bool``) are built separately below."""


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.nu`` colour-config module per theme."""
    lines = [
        theme.header("Nushell colour-config module").rstrip("\n"),
        "# Save under themes/ and source it, or point SPACECRAFT_THEME at its",
        "# slug — see INSTALL.md.",
        "",
        "export def main [] {",
        "    return {",
    ]

    body: list[str] = [_plain(theme, key, role) for key, role in _TOP_PLAIN]
    body += [_bold(theme, key, role) for key, role in _TOP_BOLD]
    body.append(f"bool: {{ || if $in {{ {_v(theme, 'success')} }} else {{ {_v(theme, 'error')} }} }}")
    body.append(_fill(theme, "search_result", "background", "accent"))
    body += [_plain(theme, key, role) for key, role in _SHAPE_PLAIN]
    body.append(_fill(theme, "shape_garbage", "background", "error", bold=True))

    lines += [f"        {entry}" for entry in body]
    lines += [
        "    }",
        "}",
        "",
    ]
    return {f"themes/{theme.slug}.nu": "\n".join(lines)}


TARGET = Target(
    id="nushell",
    target_dir="Shells/Nushell",
    render=render,
    supports_mono=True,
    legacy_files=("config.nu",),
    description="Nushell $env.config.color_config modules (themes/<slug>.nu)",
)
