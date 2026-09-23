# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Windows Terminal colour schemes.

Renders one scheme per theme into JSON compatible with Windows Terminal's
schemes array in settings.json. The render_bundle output (schemes.json)
collects all themes for pasting into the settings file.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from steelbore_themes.core import Theme


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.json`` per theme.

    Windows Terminal scheme format: name, background, foreground, cursorColor,
    selectionBackground, black, red, green, yellow, blue, purple, cyan, white,
    brightBlack, brightRed, brightGreen, brightYellow, brightBlue,
    brightPurple, brightCyan, brightWhite.
    """
    scheme: dict[str, str] = {
        "name": theme.name,
        "background": theme.background,
        "foreground": theme.foreground,
        "cursorColor": theme.focus,
        "selectionBackground": theme.accent,
        "black": theme.ansi["black"],
        "red": theme.ansi["red"],
        "green": theme.ansi["green"],
        "yellow": theme.ansi["yellow"],
        "blue": theme.ansi["blue"],
        "purple": theme.ansi["magenta"],
        "cyan": theme.ansi["cyan"],
        "white": theme.ansi["white"],
        "brightBlack": theme.ansi_bright["black"],
        "brightRed": theme.ansi_bright["red"],
        "brightGreen": theme.ansi_bright["green"],
        "brightYellow": theme.ansi_bright["yellow"],
        "brightBlue": theme.ansi_bright["blue"],
        "brightPurple": theme.ansi_bright["magenta"],
        "brightCyan": theme.ansi_bright["cyan"],
        "brightWhite": theme.ansi_bright["white"],
    }
    return {f"themes/{theme.slug}.json": json.dumps(scheme, indent=2) + "\n"}


def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
    """The ``schemes.json`` bundle — all themes in one array.

    Windows Terminal expects schemes without alpha in the settings.json
    array, so selectionBackground uses the accent role directly.
    """
    schemes: list[dict[str, str]] = []
    for theme in themes:
        scheme: dict[str, str] = {
            "name": theme.name,
            "background": theme.background,
            "foreground": theme.foreground,
            "cursorColor": theme.focus,
            "selectionBackground": theme.accent,
            "black": theme.ansi["black"],
            "red": theme.ansi["red"],
            "green": theme.ansi["green"],
            "yellow": theme.ansi["yellow"],
            "blue": theme.ansi["blue"],
            "purple": theme.ansi["magenta"],
            "cyan": theme.ansi["cyan"],
            "white": theme.ansi["white"],
            "brightBlack": theme.ansi_bright["black"],
            "brightRed": theme.ansi_bright["red"],
            "brightGreen": theme.ansi_bright["green"],
            "brightYellow": theme.ansi_bright["yellow"],
            "brightBlue": theme.ansi_bright["blue"],
            "brightPurple": theme.ansi_bright["magenta"],
            "brightCyan": theme.ansi_bright["cyan"],
            "brightWhite": theme.ansi_bright["white"],
        }
        schemes.append(scheme)
    return {"schemes.json": json.dumps({"schemes": schemes}, indent=2) + "\n"}


TARGET = Target(
    id="windows_terminal",
    target_dir="Terminals/Windows_Terminal",
    render=render,
    render_bundle=render_bundle,
    supports_mono=False,
    legacy_files=("spacecraft-software.json", "settings.json"),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-windows_terminal.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Windows Terminal colour schemes (include themes/<slug>.json and bundle schemes.json)",
)
