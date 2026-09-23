# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""MATE desktop — GTK3 panel CSS and Metacity window-border theme renderer.

Two files per theme: ``gtk.css`` (the MATE panel rules plus a GTK3
``@define-color`` token set for the wider desktop) and
``metacity-theme-1.xml`` (Metacity window-border geometry and colours).
Neither format carries a hex literal of its own; every colour is read from
the :class:`Theme` through a role accessor.

MATE's panel and Metacity have no functional per-file light/dark flag of
their own — like GNOME, MATE resolves light/dark from the desktop's own
appearance setting, not from anything a theme file declares — so a light
theme's polarity is recorded here only as a documentation comment (see
``tools/README.md`` rule 8).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def _define(name: str, value: str) -> str:
    return f"@define-color {name} {value};"


def _render_gtk_css(theme: Theme) -> str:
    """``gtk.css`` — MATE panel rules plus GTK3 legacy colour names."""
    lines = [theme.header_block("MATE panel and GTK3 colour tokens").rstrip("\n"), ""]
    if theme.is_light:
        lines += [
            f"/* Canvas polarity: light ({theme.slug}). MATE reads light/dark",
            "   from the desktop's own appearance setting, not from this file —",
            "   see tools/README.md. */",
            "",
        ]

    lines += [
        "/* MATE Panel Specifics */",
        ".mate-panel-menu-bar,",
        ".mate-panel-applet-slider,",
        ".mate-panel-applet {",
        f"  background-color: {theme.background};",
        f"  color: {theme.foreground};",
        "  font-weight: bold;",
        "}",
        "",
        "/* Active Window List Item in Panel: a surface fill with an inset",
        "   accent underline — the fill's own text is the foreground, the",
        "   verified pairing for that surface (§11.0.1). */",
        ".mate-panel-applet button:checked {",
        f"  background-color: {theme.surface};",
        f"  box-shadow: inset 0 -2px 0 {theme.accent};",
        f"  color: {theme.foreground};",
        "}",
        "",
        "/* Panel menu items */",
        ".mate-panel-menu-bar menuitem:hover,",
        ".mate-panel-applet button:hover {",
        f"  background-color: {theme.surface};",
        f"  color: {theme.foreground};",
        "}",
        "",
        "/* Clock and Status Icons */",
        "#ClockApplet-button,",
        "#NaTrayApplet-button {",
        f"  color: {theme.success};",
        "}",
        "",
        "/* Tooltips */",
        "tooltip {",
        f"  background-color: {theme.surface};",
        f"  color: {theme.foreground};",
        f"  border: 1px solid {theme.border};",
        "}",
        "",
        "/* GTK3 legacy colour names (Caja, MATE control panels, and any",
        "   other non-libadwaita application resolve theme colour through",
        "   these). */",
        _define("theme_bg_color", theme.background),
        _define("theme_fg_color", theme.foreground),
        _define("theme_selected_bg_color", theme.accent),
        _define("theme_selected_fg_color", theme.background),
        _define("theme_selected_borders_color", theme.accent),
        _define("theme_base_color", theme.surface_alt),
        _define("theme_text_color", theme.foreground),
        _define("borders", theme.border),
        _define("warning_color", theme.warning),
        _define("error_color", theme.error),
        _define("success_color", theme.success),
        "",
        "/* Insensitive / disabled widgets: structure, never a surface fill",
        "   (surface tokens are fills only, never text — §11.0.1). */",
        _define("insensitive_fg_color", theme.structure),
        _define("insensitive_bg_color", theme.surface),
        "",
        "/* Content views (file manager panes, text views) */",
        _define("content_view_bg", theme.surface_alt),
        _define("tooltip_bg_color", theme.surface),
        _define("tooltip_fg_color", theme.foreground),
        "",
        "/* Unfocused window state: same roles, dimmed via structure for text */",
        _define("theme_unfocused_bg_color", theme.background),
        _define("theme_unfocused_fg_color", theme.structure),
        _define("unfocused_borders_color", theme.border),
        "",
        "/* Focus outline: the focus role, not the accent (§11.1 rule 4). */",
        "*:focus {",
        f"  outline-color: {theme.focus};",
        "}",
        "",
    ]
    return "\n".join(lines) + "\n"


def _render_metacity_xml(theme: Theme) -> str:
    """``metacity-theme-1.xml`` — window-border geometry and colours."""
    header = theme.header_block("MATE Metacity window border theme", "<!--", "-->").rstrip("\n")
    lines = [
        '<?xml version="1.0"?>',
        header,
        "<metacity_theme>",
        "<info>",
        "  <name>Spacecraft Software</name>",
        "  <author>Mohamed Hammad</author>",
        "  <copyright>Mohamed Hammad (GPL-3.0-or-later)</copyright>",
        f"  <description>{theme.name}. URL: https://SpacecraftSoftware.org</description>",
        "</info>",
        "",
        '<frame_geometry name="normal" has_title="true" title_scale="medium" parent="normal_base">',
        '  <distance name="left_width" value="1"/>',
        '  <distance name="right_width" value="1"/>',
        '  <distance name="bottom_height" value="1"/>',
        '  <distance name="left_titlebar_edge" value="1"/>',
        '  <distance name="right_titlebar_edge" value="1"/>',
        '  <distance name="title_vertical_pad" value="4"/>',
        '  <border name="title_border" left="2" right="2" top="2" bottom="2"/>',
        '  <border name="button_border" left="0" right="0" top="0" bottom="0"/>',
        "</frame_geometry>",
        "",
        '<draw_ops name="draw_title_text">',
        f'  <title color="{theme.foreground}" x="0" y="0"/>',
        "</draw_ops>",
        "",
        '<draw_ops name="draw_frame_normal">',
        f'  <rectangle color="{theme.background}" x="0" y="0" width="width" height="height" filled="true"/>',
        f'  <rectangle color="{theme.border}" x="0" y="0" width="width" height="height" filled="false"/>',
        f'  <rectangle color="{theme.surface}" x="1" y="1" width="width-2" height="title_height" filled="true"/>',
        f'  <line color="{theme.border}" x1="0" y1="title_height" x2="width" y2="title_height"/>',
        "</draw_ops>",
        "",
        '<frame_style name="normal" geometry="normal">',
        '  <piece position="entire_background" draw_ops="draw_frame_normal"/>',
        '  <piece position="title" draw_ops="draw_title_text"/>',
        "</frame_style>",
        "",
        "<!-- Focused variant: the same geometry with an accent border, so a",
        "     window manager that distinguishes focus state has a style to",
        "     switch to without redefining geometry. -->",
        '<draw_ops name="draw_frame_focused">',
        f'  <rectangle color="{theme.background}" x="0" y="0" width="width" height="height" filled="true"/>',
        f'  <rectangle color="{theme.accent}" x="0" y="0" width="width" height="height" filled="false"/>',
        f'  <rectangle color="{theme.surface}" x="1" y="1" width="width-2" height="title_height" filled="true"/>',
        f'  <line color="{theme.accent}" x1="0" y1="title_height" x2="width" y2="title_height"/>',
        "</draw_ops>",
        "",
        '<frame_style name="focused" geometry="normal">',
        '  <piece position="entire_background" draw_ops="draw_frame_focused"/>',
        '  <piece position="title" draw_ops="draw_title_text"/>',
        "</frame_style>",
        "",
        '<window type="normal" style_set="normal"/>',
        "</metacity_theme>",
        "",
    ]
    return "\n".join(lines)


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>/{gtk.css, metacity-theme-1.xml}`` pair per theme."""
    return {
        f"themes/{theme.slug}/gtk.css": _render_gtk_css(theme),
        f"themes/{theme.slug}/metacity-theme-1.xml": _render_metacity_xml(theme),
    }


TARGET = Target(
    id="mate",
    target_dir="Desktops/MATE",
    render=render,
    supports_mono=False,
    legacy_files=("gtk.css", "metacity-theme-1.xml"),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-mate.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-mate-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="MATE: panel CSS + Metacity borders (themes/<slug>/gtk.css, metacity-theme-1.xml)",
)
