# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Zed editor — theme family renderer.

Renders the Steelbore palette family into Zed's theme-family JSON schema
(https://zed.dev/schema/themes/v0.2.0.json). Every colour is an 8-digit
``#rrggbbff`` hex built from a :class:`Theme` role via ``with_alpha`` (opaque
fills use alpha ``ff``; translucent fills use a lower alpha). One
``themes/<slug>.json`` family file per theme holds exactly one theme entry;
``render_bundle`` additionally produces ``steelbore.json``, a single family
named ``Steelbore`` holding every theme, default first.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

_SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"
_AUTHOR = "Mohamed Hammad"


def _hexa(value: str, alpha: str) -> str:
    """Append a two-digit alpha suffix to an already-resolved role hex.

    Used for the handful of colours (``text_safe_accent``) that are computed
    properties rather than a direct ``Theme.roles`` key, so
    :meth:`Theme.with_alpha` (which only indexes ``roles``) cannot reach them.
    """
    return f"{value}{alpha.upper()}"


def _style(theme: Theme) -> dict[str, object]:
    """The ``style`` object for one theme entry."""
    a = theme.with_alpha
    text_accent = _hexa(theme.text_safe_accent, "FF")

    style: dict[str, object] = {
        # Chrome background (window edges, panes) vs. the editor canvas —
        # Zed's root "background" is the app chrome, not the content canvas
        # (that is "surface.background" below); §11.1's surface role fits it.
        "background": a("surface", "FF"),
        "border": a("structure", "FF"),
        "border.variant": a("structure", "60"),
        "border.focused": a("focus", "FF"),
        "border.selected": a("accent", "FF"),
        "border.transparent": a("background", "00"),
        "border.disabled": a("structure", "40"),
        "elevated_surface.background": a("surface", "FF"),
        "surface.background": a("background", "FF"),
        "element.background": a("surface", "FF"),
        "element.hover": a("surface-alt", "FF"),
        "element.active": a("accent", "40"),
        "element.selected": a("accent", "40"),
        "element.disabled": a("surface", "FF"),
        "drop_target.background": a("accent", "40"),
        "ghost_element.background": a("background", "00"),
        "ghost_element.hover": a("surface-alt", "40"),
        "ghost_element.active": a("accent", "40"),
        "ghost_element.selected": a("accent", "40"),
        "ghost_element.disabled": a("surface", "80"),
        "text": a("foreground", "FF"),
        "text.muted": a("structure", "FF"),
        "text.placeholder": a("structure", "80"),
        "text.disabled": a("structure", "60"),
        "text.accent": text_accent,
        "icon": a("foreground", "FF"),
        "icon.muted": a("structure", "FF"),
        "icon.disabled": a("structure", "60"),
        "icon.placeholder": a("structure", "80"),
        "icon.accent": a("accent", "FF"),
        "status_bar.background": a("background", "FF"),
        "title_bar.background": a("background", "FF"),
        "title_bar.inactive_background": a("surface", "FF"),
        "toolbar.background": a("background", "FF"),
        "tab_bar.background": a("surface", "FF"),
        "tab.inactive_background": a("surface", "FF"),
        "tab.active_background": a("background", "FF"),
        "search.match_background": a("accent", "40"),
        "panel.background": a("surface", "FF"),
        "panel.focused_border": a("focus", "FF"),
        "pane.focused_border": a("focus", "FF"),
        "scrollbar.thumb.background": a("structure", "30"),
        "scrollbar.thumb.hover_background": a("structure", "50"),
        "scrollbar.thumb.border": a("background", "00"),
        "scrollbar.track.background": a("background", "00"),
        "scrollbar.track.border": a("background", "00"),
        "editor.foreground": a("foreground", "FF"),
        "editor.background": a("background", "FF"),
        "editor.gutter.background": a("background", "FF"),
        "editor.subheader.background": a("surface", "FF"),
        "editor.active_line.background": a("surface", "FF"),
        "editor.highlighted_line.background": a("accent", "20"),
        "editor.line_number": a("structure", "FF"),
        "editor.active_line_number": a("foreground", "FF"),
        "editor.invisible": a("structure", "40"),
        "editor.wrap_guide": a("structure", "20"),
        "editor.active_wrap_guide": a("structure", "40"),
        # Beyond the legacy key set — real Zed schema keys the hand-written
        # file did not cover (rule: cover more than the legacy file).
        "editor.indent_guide": a("structure", "20"),
        "editor.indent_guide_active": a("structure", "50"),
        "editor.document_highlight.read_background": a("focus", "20"),
        "editor.document_highlight.write_background": a("warning", "20"),
        "editor.hover.background": a("surface", "FF"),
        "terminal.background": a("background", "FF"),
        "terminal.foreground": a("foreground", "FF"),
        "terminal.bright_foreground": a("foreground", "FF"),
        "terminal.dim_foreground": a("structure", "FF"),
        "link_text.hover": a("structure", "FF"),
    }

    for slot in ANSI_SLOTS:
        # theme.ansi / theme.ansi_bright already resolve to role hexes
        # (§11.1 ANSI derivation, core.py); just append the opaque alpha.
        style[f"terminal.ansi.{slot}"] = _hexa(theme.ansi[slot], "FF")
        style[f"terminal.ansi.bright_{slot}"] = _hexa(theme.ansi_bright[slot], "FF")

    # VCS / diagnostic status triples: base, .background (translucent fill),
    # .border. Git/diagnostic semantics mapped onto the closest §11.1 role.
    status_roles = {
        "conflict": "error",
        "created": "success",
        "deleted": "error",
        "error": "error",
        "hidden": "structure",
        "hint": "structure",
        "ignored": "structure",
        "modified": "warning",
        "predictive": "structure",
        "renamed": "focus",
        "success": "success",
        "unreachable": "structure",
        "warning": "warning",
    }
    for key, role in status_roles.items():
        style[key] = a(role, "FF")
        style[f"{key}.background"] = a(role, "20")
        style[f"{key}.border"] = a(role, "FF")

    # "info" is a computed property (Classic's real Liquid Coolant value;
    # ``structure`` for every eleven-role palette — core.py, README rule 6),
    # not a plain ``roles`` entry, so it cannot go through ``with_alpha``
    # like the table above; read it directly, same as ``text_safe_accent``.
    info_hex = _hexa(theme.info, "FF")
    style["info"] = info_hex
    style["info.background"] = _hexa(theme.info, "20")
    style["info.border"] = info_hex

    style["players"] = [
        {
            "cursor": a("foreground", "FF"),
            "background": a("accent", "FF"),
            "selection": a("accent", "40"),
        }
    ]

    style["syntax"] = {
        "attribute": {"color": a("success", "FF")},
        "boolean": {"color": a("warning", "FF")},
        "comment": {"color": a("structure", "FF"), "font_style": "italic"},
        "comment.doc": {"color": a("structure", "FF"), "font_style": "italic"},
        "constant": {"color": a("warning", "FF")},
        "constructor": {"color": a("focus", "FF")},
        "embedded": {"color": a("foreground", "FF")},
        "emphasis": {"font_style": "italic"},
        "emphasis.strong": {"font_weight": 700},
        "enum": {"color": a("focus", "FF")},
        "function": {"color": a("focus", "FF")},
        "hint": {"color": a("structure", "FF")},
        "keyword": {"color": text_accent, "font_weight": 700},
        "label": {"color": a("structure", "FF")},
        "link_text": {"color": a("structure", "FF")},
        "link_uri": {"color": a("structure", "FF")},
        "number": {"color": a("warning", "FF")},
        "operator": {"color": a("foreground", "FF")},
        "predictive": {"color": a("structure", "80")},
        "preproc": {"color": a("structure", "FF")},
        "primary": {"color": a("foreground", "FF")},
        "property": {"color": a("success", "FF")},
        "punctuation": {"color": a("foreground", "FF")},
        "punctuation.bracket": {"color": a("foreground", "FF")},
        "punctuation.delimiter": {"color": a("foreground", "FF")},
        "punctuation.list_marker": {"color": a("warning", "FF")},
        "punctuation.special": {"color": a("structure", "FF")},
        "string": {"color": a("success", "FF")},
        "string.escape": {"color": a("error", "FF")},
        "string.regex": {"color": a("error", "FF")},
        "string.special": {"color": a("success", "FF")},
        "string.special.symbol": {"color": a("success", "FF")},
        "tag": {"color": a("error", "FF")},
        "text.literal": {"color": a("success", "FF")},
        "title": {"color": a("accent", "FF"), "font_weight": 700},
        "type": {"color": a("structure", "FF")},
        "variable": {"color": a("foreground", "FF")},
        "variable.special": {"color": a("focus", "FF")},
        "variant": {"color": a("focus", "FF")},
    }

    return style


def _theme_entry(theme: Theme) -> dict[str, object]:
    return {
        "name": theme.name,
        "appearance": "dark" if theme.is_dark else "light",
        "style": _style(theme),
    }


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.json`` family file per theme, exactly one entry."""
    family = {
        "$schema": _SCHEMA,
        "name": theme.name,
        "author": _AUTHOR,
        "themes": [_theme_entry(theme)],
    }
    return {f"themes/{theme.slug}.json": json.dumps(family, indent=2) + "\n"}


def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
    """``steelbore.json`` — one family named ``Steelbore``, every theme, default first."""
    family = {
        "$schema": _SCHEMA,
        "name": "Steelbore",
        "author": _AUTHOR,
        "themes": [_theme_entry(theme) for theme in themes],
    }
    return {"steelbore.json": json.dumps(family, indent=2) + "\n"}


TARGET = Target(
    id="zed",
    target_dir="Editors/Zed",
    render=render,
    render_bundle=render_bundle,
    supports_mono=False,
    legacy_files=("spacecraft-software.json",),
    archives=(
        Archive(
            path="Editors/Zed/spacecraft-software-zed-theme.zip",
            fmt="zip",
            entries=(
                ("themes", "themes"),
                ("steelbore.json", "steelbore.json"),
                ("INSTALL.md", "INSTALL.md"),
            ),
        ),
    ),
    description="Zed editor theme family (themes/<slug>.json plus bundle steelbore.json)",
)
