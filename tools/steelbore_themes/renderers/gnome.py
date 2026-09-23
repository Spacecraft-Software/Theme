# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""GNOME desktop — libadwaita ``gtk.css`` and GNOME Shell CSS renderer.

Two files per theme: ``gtk.css`` (a flat ``@define-color`` token sheet
consumed by libadwaita/GTK4 apps, plus the GTK3 legacy colour names for
older applications) and ``gnome-shell.css`` (a handful of shell-chrome
rules — panel, popup menu, calendar). Neither format carries a hex literal
of its own; every colour is read from the :class:`Theme` through a role
accessor. Translucent "shade" fills use ``theme.rgb("background")`` composed
into ``rgba()`` rather than a hex-plus-alpha string, matching how libadwaita
itself expresses ``*_shade_color``.

GTK has no functional per-stylesheet light/dark flag — GNOME resolves
light/dark from the ``org.gnome.desktop.interface color-scheme`` portal
setting, not from anything a theme's CSS declares — so a light theme's
polarity is recorded here only as a documentation comment (see
``tools/README.md`` rule 8 and the module notes returned by the caller).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme

_SHADE_ALPHA = 0.36
"""Opacity for libadwaita's ``*_shade_color`` tokens — a UI convention
constant (matching the legacy hand-written sheet), not a colour value."""


def _shade(theme: Theme) -> str:
    """``rgba(r, g, b, alpha)`` over the theme's background — never a hex."""
    r, g, b = theme.rgb("background")
    return f"rgba({r}, {g}, {b}, {_SHADE_ALPHA})"


def _define(name: str, value: str) -> str:
    return f"@define-color {name} {value};"


def _render_gtk_css(theme: Theme) -> str:
    """``gtk.css`` — libadwaita named colours plus GTK3 legacy names."""
    shade = _shade(theme)
    lines = [theme.header_block("GTK / libadwaita colour tokens").rstrip("\n"), ""]
    if theme.is_light:
        lines += [
            f"/* Canvas polarity: light ({theme.slug}). GTK reads light/dark",
            "   from the desktop portal, not from this file — see tools/README.md. */",
            "",
        ]

    lines += ["/* Accent */"]
    lines += [
        _define("accent_color", theme.accent),
        _define("accent_bg_color", theme.accent),
        _define("accent_fg_color", theme.background),
        "",
        "/* Destructive / error */",
        _define("destructive_color", theme.error),
        _define("destructive_bg_color", theme.error),
        _define("destructive_fg_color", theme.background),
        _define("error_color", theme.error),
        _define("error_bg_color", theme.error),
        _define("error_fg_color", theme.background),
        "",
        "/* Success */",
        _define("success_color", theme.success),
        _define("success_bg_color", theme.success),
        _define("success_fg_color", theme.background),
        "",
        "/* Warning. success/destructive/accent fills pair with background text",
        "   -- the allowed inversion tools/README.md rule 3 verifies (accent,",
        "   structure, success, error only). warning is not on that list: no",
        "   role is a verified pairing against the warning fill in every",
        "   registered palette (Solarized's warning hue fails AA against its",
        "   own background at 2.98:1), so warning_fg_color is left undefined",
        "   here and libadwaita falls back to its own built-in default, which",
        "   is a fixed near-black tone designed for text on a saturated",
        "   warning fill rather than anything this theme resolves. */",
        _define("warning_color", theme.warning),
        _define("warning_bg_color", theme.warning),
        "",
        "/* Window / view */",
        _define("window_bg_color", theme.background),
        _define("window_fg_color", theme.foreground),
        _define("view_bg_color", theme.surface_alt),
        _define("view_fg_color", theme.foreground),
        "",
        "/* Headerbar */",
        _define("headerbar_bg_color", theme.surface),
        _define("headerbar_fg_color", theme.foreground),
        _define("headerbar_border_color", theme.border),
        _define("headerbar_backdrop_color", theme.background),
        _define("headerbar_shade_color", shade),
        "",
        "/* Cards / popovers / dialogs */",
        _define("card_bg_color", theme.surface),
        _define("card_fg_color", theme.foreground),
        _define("card_shade_color", shade),
        _define("popover_bg_color", theme.surface),
        _define("popover_fg_color", theme.foreground),
        _define("dialog_bg_color", theme.surface),
        _define("dialog_fg_color", theme.foreground),
        "",
        "/* Sidebars */",
        _define("sidebar_bg_color", theme.surface),
        _define("sidebar_fg_color", theme.foreground),
        _define("sidebar_backdrop_color", theme.background),
        _define("sidebar_shade_color", shade),
        _define("secondary_sidebar_bg_color", theme.surface),
        _define("secondary_sidebar_fg_color", theme.foreground),
        _define("secondary_sidebar_backdrop_color", theme.background),
        _define("secondary_sidebar_shade_color", shade),
        "",
        "/* Thumbnails / misc fills */",
        _define("thumbnail_bg_color", theme.surface),
        _define("thumbnail_fg_color", theme.foreground),
        _define("shade_color", shade),
        _define("scrollbar_outline_color", theme.border),
        _define("borders", theme.border),
        "",
        "/* GTK3 legacy names (older, non-libadwaita applications) */",
        _define("theme_bg_color", theme.background),
        _define("theme_fg_color", theme.foreground),
        _define("theme_selected_bg_color", theme.accent),
        _define("theme_selected_fg_color", theme.background),
        _define("theme_base_color", theme.surface_alt),
        _define("theme_text_color", theme.foreground),
        _define("insensitive_fg_color", theme.structure),
        "",
        "/* Focus outline: the focus role, not the accent (§11.1 rule 4). */",
        "*:focus,",
        "*:focus-visible {",
        f"  outline-color: {theme.focus};",
        "}",
        "",
    ]
    return "\n".join(lines) + "\n"


def _render_gnome_shell_css(theme: Theme) -> str:
    """``gnome-shell.css`` — minimal shell-chrome rules."""
    lines = [theme.header_block("GNOME Shell theme").rstrip("\n"), ""]
    if theme.is_light:
        lines += [f"/* Canvas polarity: light ({theme.slug}). */", ""]
    lines += [
        "#panel {",
        f"  background-color: {theme.background};",
        "  font-weight: bold;",
        "  height: 32px;",
        "}",
        "",
        ".panel-button {",
        f"  color: {theme.foreground};",
        "}",
        "",
        ".panel-button:hover {",
        f"  background-color: {theme.surface};",
        f"  box-shadow: inset 0 -2px 0 {theme.accent};",
        f"  color: {theme.foreground};",
        "}",
        "",
        ".popup-menu {",
        f"  background-color: {theme.surface};",
        f"  color: {theme.foreground};",
        "}",
        "",
        ".popup-menu-item:hover {",
        f"  background-color: {theme.surface_alt};",
        "}",
        "",
        ".calendar {",
        f"  background-color: {theme.surface};",
        f"  color: {theme.foreground};",
        "}",
        "",
        ".calendar-day-base {",
        f"  color: {theme.foreground};",
        "}",
        "",
        ".calendar-today {",
        f"  background-color: {theme.accent};",
        f"  color: {theme.background};",
        "}",
        "",
    ]
    return "\n".join(lines) + "\n"


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>/{gtk.css, gnome-shell.css}`` pair per theme."""
    return {
        f"themes/{theme.slug}/gtk.css": _render_gtk_css(theme),
        f"themes/{theme.slug}/gnome-shell.css": _render_gnome_shell_css(theme),
    }


TARGET = Target(
    id="gnome",
    target_dir="Desktops/GNOME",
    render=render,
    supports_mono=False,
    legacy_files=("gtk.css", "gnome-shell.css"),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-gnome.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-gnome-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="GNOME / libadwaita GTK4 colour tokens and GNOME Shell chrome",
)
