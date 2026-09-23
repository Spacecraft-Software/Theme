# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Lapce editor — colour theme TOML renderer.

Lapce colour themes are TOML documents consumed by the editor's theme loader:
a ``[theme]`` metadata block, ``[color-theme.ui]`` (chrome, panels, status
bar, tabs), ``[color-theme.syntax]`` (highlighting) and ``[color-theme.terminal]``
(the embedded terminal's ANSI palette). Every colour is a §11.1 role token off
a :class:`Theme`; translucent fills use :meth:`Theme.with_alpha`, or the local
``_hexa`` helper for the one colour (``text_safe_accent``) that is a computed
property rather than a direct ``Theme.roles`` key, so ``with_alpha`` cannot
index it directly.

Every legacy key (``git show HEAD:Editors/Lapce/spacecraft-software.toml``)
is present under a modern-Lapce name, plus additional keys the legacy file
never had. Renames, not drops: ``editor.current-line`` ->
``editor.current_line``, ``editor.line-number``/``active-line-number`` ->
``editor.line_number``/``active_line_number``, ``editor.sticky-header.background``
-> ``editor.sticky_header_background``, ``panel.foreground.dim`` unchanged,
``tab.*`` -> ``lapce.tab.*``, ``scroll-bar`` -> ``lapce.scroll_bar``,
``source-control.*`` -> ``source_control.*``, top-level ``error``/``warn`` ->
``lapce.error``/``lapce.warn`` (plus an ``error_lens.*`` family the legacy
file lacked), bare ``link`` is kept alongside the new ``editor.link``. The
Font styles: the legacy hand-written file used Lapce's older structured
``{ color = ..., bold = ..., italic = ... }`` syntax values; current upstream
Lapce themes (``defaults/dark-theme.toml``) declare syntax entries as bare
colour strings, so bold/italic emphasis is intentionally not emitted and
``markup.bold`` / ``markup.italic`` carry the plain foreground.

one legacy key with no 1:1 role (``panel.hovered.active.foreground``, an
invented Steel Orange with no role) is restored as ``theme.text_safe_accent``
rather than dropped. ``[color-theme.terminal]`` keys are bare
(``background``/``black``/``bright_black``/...) — no ``terminal.`` prefix,
since the table header already supplies that namespace; word-joining is
underscore per current upstream Lapce, not the legacy file's dashes.
Status-bar modal fills use only the four roles rule 3 of ``tools/README.md``
allows for background-coloured text (``accent``/``structure``/``success``/
``error``) — never ``focus``/``warning``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, MAINTAINER, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

_AUTHOR = MAINTAINER


def _hexa(value: str, alpha: str) -> str:
    """Append a two-digit alpha suffix to an already-resolved role hex.

    Needed for colours built from a computed property (``text_safe_accent``)
    rather than a direct ``Theme.roles`` key, which is all
    :meth:`Theme.with_alpha` can index.
    """
    return f"{value}{alpha.upper()}"


def _kv(key: str, value: str) -> str:
    """One ``"dotted.key" = "value"`` TOML line.

    Upstream Lapce theme files always quote dotted keys, so every key is
    quoted here regardless of whether it actually contains a dot.
    """
    return f'"{key}" = "{value}"'


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.toml`` per theme."""
    a = theme.with_alpha
    accent_text = theme.text_safe_accent

    lines = [theme.header("Lapce colour theme").rstrip("\n"), ""]

    # -- [theme] metadata -----------------------------------------------------
    lines += [
        "[theme]",
        f'name = "{theme.name}"',
        f'author = "{_AUTHOR}"',
        f'color-theme.name = "{theme.name}"',
        f'color-theme.type = "{"dark" if theme.is_dark else "light"}"',
        "",
    ]

    # -- [color-theme.ui] -------------------------------------------------------
    lines.append("[color-theme.ui]")
    lines.append("# Editor")
    lines += [
        _kv("editor.background", theme.background),
        _kv("editor.foreground", theme.foreground),
        _kv("editor.dim", theme.structure),
        _kv("editor.focus", theme.focus),
        _kv("editor.caret", theme.foreground),
        _kv("editor.selection", _hexa(accent_text, "40")),
        _kv("editor.current_line", theme.surface),
        _kv("editor.debug_break_line", a("warning", "40")),
        _kv("editor.link", theme.structure),
        _kv("editor.visible_whitespace", a("structure", "40")),
        _kv("editor.indent_guide", a("structure", "20")),
        _kv("editor.drag_drop_background", _hexa(accent_text, "40")),
        _kv("editor.drag_drop_tab_background", a("surface-alt", "40")),
        _kv("editor.sticky_header_background", theme.surface),
        _kv("editor.line_number", theme.structure),
        _kv("editor.active_line_number", theme.foreground),
        "",
        "# Top-level link (legacy bare key, kept alongside editor.link)",
        _kv("link", theme.structure),
        "",
        "# Inlay hints / error lens / completion lens",
        _kv("inlay_hint.foreground", theme.structure),
        _kv("inlay_hint.background", a("focus", "20")),
        _kv("error_lens.error.foreground", theme.error),
        _kv("error_lens.error.background", a("error", "20")),
        _kv("error_lens.warning.foreground", theme.warning),
        _kv("error_lens.warning.background", a("warning", "20")),
        _kv("error_lens.other.foreground", theme.structure),
        _kv("error_lens.other.background", a("structure", "20")),
        _kv("completion_lens.foreground", theme.structure),
        "",
        "# Panel",
        _kv("panel.background", theme.surface),
        _kv("panel.foreground", theme.foreground),
        _kv("panel.foreground.dim", theme.structure),
        _kv("panel.current.background", _hexa(accent_text, "40")),
        _kv("panel.current.foreground", theme.foreground),
        _kv("panel.current.foreground.dim", theme.structure),
        _kv("panel.hovered.background", theme.surface_alt),
        _kv("panel.hovered.active.background", theme.surface),
        _kv("panel.hovered.active.foreground", accent_text),
        _kv("panel.hovered.foreground", theme.foreground),
        _kv("panel.hovered.foreground.dim", theme.structure),
        "",
        "# Status bar — modal fills use background-coloured text on a role",
        "# fill, the one inversion rule 3 allows (background text on an",
        "# accent/structure/success/error fill); each of the four modes",
        "# takes a distinct role from that exact list, never focus/warning.",
        _kv("status.background", theme.background),
        _kv("status.foreground", theme.structure),
        _kv("status.modal.normal.background", theme.structure),
        _kv("status.modal.normal.foreground", theme.background),
        _kv("status.modal.insert.background", theme.success),
        _kv("status.modal.insert.foreground", theme.background),
        _kv("status.modal.visual.background", theme.error),
        _kv("status.modal.visual.foreground", theme.background),
        _kv("status.modal.terminal.background", accent_text),
        _kv("status.modal.terminal.foreground", theme.background),
        "",
        "# Tabs — underline is decorative (rule 4: plain accent is fine for",
        "# non-text fills/borders/icons); the active label is text, so it",
        "# takes the text-safe accent.",
        _kv("lapce.tab.active.background", theme.background),
        _kv("lapce.tab.active.foreground", accent_text),
        _kv("lapce.tab.active.underline", theme.accent),
        _kv("lapce.tab.inactive.background", theme.surface),
        _kv("lapce.tab.inactive.foreground", theme.structure),
        _kv("lapce.tab.inactive.underline", a("accent", "77")),
        _kv("lapce.tab.separator", theme.border),
        "",
        "# Scroll bar / dropdown shadow / border",
        _kv("lapce.scroll_bar", a("structure", "70")),
        _kv("lapce.dropdown_shadow", a("background", "80")),
        _kv("lapce.border", theme.border),
        "",
        "# Buttons — the fill takes the text-safe accent so the background-",
        "# coloured label on top (the allowed inversion, rule 3) stays a",
        "# verified pairing even under Steelbore Blue's restricted accent.",
        _kv("lapce.button.primary.background", accent_text),
        _kv("lapce.button.primary.foreground", theme.background),
        "",
        "# Icons",
        _kv("lapce.icon.active", theme.foreground),
        _kv("lapce.icon.inactive", theme.structure),
        "",
        "# Remote status",
        _kv("lapce.remote.icon", theme.background),
        _kv("lapce.remote.local", theme.structure),
        _kv("lapce.remote.connected", theme.success),
        _kv("lapce.remote.connecting", theme.warning),
        _kv("lapce.remote.disconnected", theme.error),
        "",
        "# Plugin list",
        _kv("lapce.plugin.name", theme.foreground),
        _kv("lapce.plugin.description", theme.structure),
        _kv("lapce.plugin.author", theme.structure),
        "",
        "# Top-level status aliases",
        _kv("lapce.error", theme.error),
        _kv("lapce.warn", theme.warning),
        "",
        "# Source control",
        _kv("source_control.added", a("success", "CC")),
        _kv("source_control.removed", a("error", "CC")),
        _kv("source_control.modified", a("warning", "CC")),
        "",
        "# Tooltip / palette / completion / hover",
        _kv("tooltip.background", theme.surface),
        _kv("tooltip.foreground", theme.foreground),
        _kv("palette.background", theme.surface),
        _kv("palette.foreground", theme.foreground),
        _kv("palette.current.background", _hexa(accent_text, "40")),
        _kv("palette.current.foreground", theme.foreground),
        _kv("completion.background", theme.surface),
        _kv("completion.current", _hexa(accent_text, "40")),
        _kv("hover.background", theme.surface),
        "",
        "# Activity bar",
        _kv("activity.background", theme.surface),
        _kv("activity.current", theme.background),
        "",
        "# Debug",
        _kv("debug.breakpoint", theme.error),
        _kv("debug.breakpoint.hover", a("error", "40")),
        "",
        "# Markdown",
        _kv("markdown.blockquote", theme.structure),
        "",
    ]

    # -- [color-theme.syntax] ----------------------------------------------------
    lines.append("[color-theme.syntax]")
    lines += [
        _kv("comment", theme.structure),
        _kv("constant", theme.warning),
        _kv("type", theme.structure),
        _kv("typeAlias", theme.structure),
        _kv("number", theme.warning),
        _kv("enum", theme.structure),
        _kv("struct", theme.structure),
        _kv("structure", theme.structure),
        _kv("interface", theme.structure),
        _kv("namespace", theme.structure),
        _kv("attribute", theme.warning),
        _kv("label", theme.warning),
        _kv("constructor", accent_text),
        _kv("function", theme.focus),
        _kv("method", theme.focus),
        _kv("function.method", theme.focus),
        _kv("keyword", accent_text),
        _kv("selfKeyword", accent_text),
        _kv("storage", accent_text),
        _kv("field", theme.foreground),
        _kv("property", theme.foreground),
        _kv("operator", theme.foreground),
        _kv("enumMember", theme.warning),
        _kv("enum-member", theme.warning),
        _kv("string", theme.success),
        _kv("type.builtin", theme.structure),
        _kv("builtinType", theme.structure),
        _kv("escape", theme.focus),
        _kv("string.escape", theme.focus),
        _kv("embedded", theme.focus),
        _kv("punctuation.delimiter", theme.structure),
        _kv("text.title", accent_text),
        _kv("text.uri", theme.structure),
        _kv("text.reference", theme.warning),
        _kv("variable", theme.foreground),
        _kv("variable.other.member", theme.foreground),
        _kv("tag", theme.error),
        "",
        _kv("markup.heading", accent_text),
        _kv("markup.bold", theme.foreground),
        _kv("markup.italic", theme.foreground),
        _kv("markup.list", theme.warning),
        _kv("markup.link.url", theme.structure),
        _kv("markup.link.label", accent_text),
        _kv("markup.link.text", accent_text),
        _kv("markup.raw", theme.success),
        "",
        _kv("bracket.color.1", theme.focus),
        _kv("bracket.color.2", theme.warning),
        _kv("bracket.color.3", accent_text),
        _kv("bracket.unpaired", theme.error),
        "",
    ]

    # -- [color-theme.terminal] ---------------------------------------------------
    # Already nested under the [color-theme.terminal] table header, so keys
    # are bare ("background", "black", "bright_black", ...) — the "terminal."
    # prefix belongs to the *upstream flat-namespace* form Lapce also accepts
    # (terminal.background at the top level), not to keys already inside this
    # table; repeating it here would double-nest to
    # color-theme.terminal.terminal.background and go unread by the loader.
    # Word-joining is underscore (bright_black, ...) per current upstream
    # Lapce, not the legacy file's dashes (bright-black).
    lines.append("[color-theme.terminal]")
    lines += [
        _kv("background", theme.background),
        _kv("foreground", theme.foreground),
        _kv("cursor", theme.foreground),
    ]
    for slot in ANSI_SLOTS:
        lines.append(_kv(slot, theme.ansi[slot]))
    for slot in ANSI_SLOTS:
        lines.append(_kv(f"bright_{slot}", theme.ansi_bright[slot]))
    lines.append("")

    return {f"themes/{theme.slug}.toml": "\n".join(lines)}


TARGET = Target(
    id="lapce",
    target_dir="Editors/Lapce",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.toml",),
    archives=(
        Archive(
            path="Editors/Lapce/spacecraft-software-lapce-theme.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Lapce editor colour themes (themes/<slug>.toml)",
)
