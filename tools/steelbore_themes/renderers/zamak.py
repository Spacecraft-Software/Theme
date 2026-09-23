# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Zamak bootloader theme — generated palette colour renderer.

Zamak reads a theme.toml configuration file to define the bootloader's colour
scheme for boot menu, status displays, and configuration editing. This renderer
generates one theme per palette variant.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.toml`` per theme."""
    lines = [theme.header("Zamak bootloader theme").rstrip("\n"), ""]

    lines += [
        "[surface]",
        f'background = "{theme.background}"',
        f'foreground = "{theme.foreground}"',
        f'dim = "{theme.structure}"',
        f'bright = "{theme.foreground}"',
        "",
        "[accent]",
        f'primary = "{theme.accent}"',
        f'secondary = "{theme.structure}"',
        f'error = "{theme.error}"',
        f'warning = "{theme.warning}"',
        f'success = "{theme.success}"',
        "",
        "[editor]",
        f'key = "{theme.structure}"',
        f'colon = "{theme.foreground}"',
        f'value = "{theme.success}"',
        f'comment = "{theme.structure}"',
        f'invalid = "{theme.error}"',
        "",
    ]

    return {f"themes/{theme.slug}.toml": "\n".join(lines) + "\n"}


TARGET = Target(
    id="zamak",
    target_dir="Bootloaders/ZAMAK",
    render=render,
    supports_mono=False,
    legacy_files=("theme.toml",),
    description="Zamak bootloader colour themes (include themes/<slug>.toml)",
)
