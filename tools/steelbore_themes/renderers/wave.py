# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Wave terminal — JSON theme renderer.

Renders the Steelbore palette family into Wave's native JSON config format.
Maps Wave's color keys to Theme roles: background/foreground for canvas,
selection colors, and 16 ANSI colours in normal and bright sets.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.json`` per theme.

    Wave terminal JSON structure with name, version, author, license, homepage,
    and terminal object containing all color assignments.
    """
    terminal = {
        "background": theme.background,
        "foreground": theme.foreground,
        "cursor": theme.focus,
        "selectionBackground": theme.text_safe_accent,
    }

    # ANSI 0–7 normal colors
    for slot in ANSI_SLOTS:
        terminal[slot] = theme.ansi[slot]

    # ANSI 8–15 bright colors
    for slot in ANSI_SLOTS:
        terminal[f"bright{slot.capitalize()}"] = theme.ansi_bright[slot]

    theme_dict = {
        "name": theme.name,
        "version": "2.0",
        "author": "Mohamed Hammad",
        "license": "GPL-3.0-or-later",
        "homepage": "https://SpacecraftSoftware.org",
        "dark": theme.is_dark,
        "terminal": terminal,
    }

    json_text = json.dumps(theme_dict, indent=2) + "\n"
    return {f"themes/{theme.slug}.json": json_text}


TARGET = Target(
    id="wave",
    target_dir="Terminals/Wave",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.json",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-wave.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Wave terminal colour themes (include themes/<slug>.json)",
)
