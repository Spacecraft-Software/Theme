# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""LeftWM window manager and Polybar theme renderer.

Renders two files per theme: ``theme.toml`` (LeftWM window manager config)
and ``polybar.config`` (Polybar status bar config). Both are TOML/INI-based
and support line comments. Colours map to the Spacecraft Software palette roles
(§11.1); no hex literal appears in the renderer.

Light themes set no polarity flag in these formats — LeftWM and Polybar read
the desktop theme from the system, not from config files. The light canvas is
documented in the rendered files via a comment for visibility.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """Render ``theme.toml`` and ``polybar.config`` for one theme."""
    theme_toml = _render_theme_toml(theme)
    polybar_config = _render_polybar_config(theme)

    return {
        f"themes/{theme.slug}/theme.toml": theme_toml,
        f"themes/{theme.slug}/polybar.config": polybar_config,
    }


def _render_theme_toml(theme: Theme) -> str:
    """LeftWM theme configuration."""
    lines = [theme.header("LeftWM window manager theme", "#").rstrip("\n"), ""]

    if theme.is_light:
        lines.append("# Canvas polarity: light")
        lines.append("")

    lines += [
        "border_width = 2",
        "margin = 4",
        "workspace_margin = 4",
        f'default_border_color = "#{theme.hex_bare("surface")}"',
        f'floating_border_color = "#{theme.hex_bare("success")}"',
        f'focused_border_color = "#{theme.hex_bare("accent")}"',
        "",
        "# Gutters (Gap between windows)",
        "gutter = [",
        '    { side = "Top", value = 0, render = false },',
        '    { side = "Bottom", value = 0, render = false },',
        '    { side = "Left", value = 0, render = false },',
        '    { side = "Right", value = 0, render = false },',
        "]",
        "",
        "[on_new_window]",
        "enabled = true",
        "",
    ]

    return "\n".join(lines) + "\n"


def _render_polybar_config(theme: Theme) -> str:
    """Polybar status bar configuration."""
    lines = [theme.header("Polybar status bar configuration", "#").rstrip("\n"), ""]

    if theme.is_light:
        lines.append("# Canvas polarity: light")
        lines.append("")

    # Color section
    lines += [
        "[colors]",
        f"background = #{theme.hex_bare('background')}",
        f"background-alt = #{theme.hex_bare('surface')}",
        f"foreground = #{theme.hex_bare('foreground')}",
        f"foreground-alt = #{theme.hex_bare('structure')}",
        f"primary = #{theme.hex_bare('accent')}",
        f"primary-text = #{theme.text_safe_accent.lstrip('#')}",
        f"secondary = #{theme.hex_bare('success')}",
        f"alert = #{theme.hex_bare('error')}",
        f"disabled = #{theme.hex_bare('structure')}",
        "",
    ]

    # Main bar configuration
    lines += [
        "[bar/main]",
        "width = 100%",
        "height = 24pt",
        "radius = 0",
        "background = ${colors.background}",
        "foreground = ${colors.foreground}",
        "line-size = 3pt",
        "border-size = 0pt",
        "padding-left = 1",
        "padding-right = 1",
        "module-margin = 1",
        "separator = |",
        "separator-foreground = ${colors.disabled}",
        'font-0 = "Inconsolata:size=10;2"',
        "",
        "modules-left = xworkspaces xwindow",
        "modules-right = filesystem pulseaudio memory cpu date",
        "",
        "cursor-click = pointer",
        "cursor-scroll = ns-resize",
        "enable-ipc = true",
        "",
    ]

    # xworkspaces module
    lines += [
        "[module/xworkspaces]",
        "type = internal/xworkspaces",
        "label-active = %name%",
        "label-active-background = ${colors.background-alt}",
        "label-active-underline = ${colors.primary}",
        "label-active-padding = 1",
        "",
        "label-occupied = %name%",
        "label-occupied-padding = 1",
        "",
        "label-urgent = %name%",
        "label-urgent-background = ${colors.alert}",
        "label-urgent-foreground = ${colors.background}",
        "label-urgent-padding = 1",
        "",
        "label-empty = %name%",
        "label-empty-foreground = ${colors.disabled}",
        "label-empty-padding = 1",
        "",
    ]

    # xwindow module
    lines += [
        "[module/xwindow]",
        "type = internal/xwindow",
        "label = %title:0:60:...%",
        "label-foreground = ${colors.primary-text}",
        "",
    ]

    # filesystem module
    lines += [
        "[module/filesystem]",
        "type = internal/fs",
        "interval = 25",
        "mount-0 = /",
        "label-mounted = %{F${colors.primary-text}}%mountpoint%%{F-} %percentage_used%%",
        "",
    ]

    # date module
    lines += [
        "[module/date]",
        "type = internal/date",
        "interval = 1",
        "date = %H:%M",
        "date-alt = %Y-%m-%d %H:%M:%S",
        "label = %date%",
        "label-foreground = ${colors.primary-text}",
        "",
    ]

    return "\n".join(lines) + "\n"


TARGET = Target(
    id="leftwm",
    target_dir="Desktops/LeftWM",
    render=render,
    supports_mono=False,
    legacy_files=("theme.toml", "polybar.config"),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-leftwm.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-leftwm-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="LeftWM + Polybar (themes/<slug>/theme.toml and themes/<slug>/polybar.config)",
)
