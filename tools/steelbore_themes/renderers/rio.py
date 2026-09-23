# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Rio terminal — TOML theme renderer.

Renders the Steelbore palette family into Rio's native TOML config format.
Maps Rio's color keys to Theme roles: background/foreground for canvas,
selection colors, and 16 ANSI colours in the normal/bright tables.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.toml`` per theme.

    Rio TOML structure:
    - [colors] for main UI colors (background, foreground, cursor, selection)
    - [colors.normal] for ANSI 0–7
    - [colors.bright] for ANSI 8–15
    """
    lines = [
        theme.header("Rio terminal theme", comment="#").rstrip("\n"),
        "",
        "[colors]",
        f'background = "{theme.background}"',
        f'foreground = "{theme.foreground}"',
        f'cursor = "{theme.focus}"',
        f'selection-background = "{theme.text_safe_accent}"',
        f'selection-foreground = "{theme.background}"',
        "",
        "[colors.normal]",
    ]

    # ANSI 0–7 normal colors
    for slot in ANSI_SLOTS:
        lines.append(f'{slot:8} = "{theme.ansi[slot]}"')

    lines += ["", "[colors.bright]"]

    # ANSI 8–15 bright colors
    for slot in ANSI_SLOTS:
        lines.append(f'{slot:8} = "{theme.ansi_bright[slot]}"')

    lines.append("")

    return {f"themes/{theme.slug}.toml": "\n".join(lines)}


TARGET = Target(
    id="rio",
    target_dir="Terminals/Rio",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.toml",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-rio.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Rio terminal colour themes (include themes/<slug>.toml)",
)
