# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""WezTerm — terminal color scheme renderer.

WezTerm color schemes are Lua tables returned from config files under
``~/.config/wezterm/colors/``. Each theme generates one ``.lua`` file.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import ANSI_SLOTS, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.lua`` per theme."""
    lines = [theme.header("WezTerm color scheme", comment="--").rstrip("\n"), ""]
    lines += [
        "return {",
        f"    foreground = {theme.foreground!r},",
        f"    background = {theme.background!r},",
        "",
        "    -- Cursor styling",
        f"    cursor_bg = {theme.focus!r},",
        f"    cursor_fg = {theme.background!r},",
        f"    cursor_border = {theme.focus!r},",
        "",
        "    -- Selection",
        f"    selection_fg = {theme.background!r},",
        f"    selection_bg = {theme.text_safe_accent!r},",
        "",
        "    -- UI elements",
        f"    scrollbar_thumb = {theme.structure!r},",
        f"    split = {theme.border!r},",
        "",
        "    -- ANSI color palette (0-7: normal, 8-15: bright)",
        "    ansi = {",
    ]
    for slot in ANSI_SLOTS:
        lines.append(f"        {theme.ansi[slot]!r},")
    lines += [
        "    },",
        "    brights = {",
    ]
    for slot in ANSI_SLOTS:
        lines.append(f"        {theme.ansi_bright[slot]!r},")
    lines += [
        "    },",
        "",
        "    -- Tab bar styling",
        "    tab_bar = {",
        f"        background = {theme.surface_alt!r},",
        "        active_tab = {",
        f"            bg_color = {theme.text_safe_accent!r},",
        f"            fg_color = {theme.background!r},",
        "        },",
        "        inactive_tab = {",
        f"            bg_color = {theme.surface!r},",
        f"            fg_color = {theme.foreground!r},",
        "        },",
        "        inactive_tab_hover = {",
        f"            bg_color = {theme.surface!r},",
        f"            fg_color = {theme.text_safe_accent!r},",
        "        },",
        "        new_tab = {",
        f"            bg_color = {theme.surface!r},",
        f"            fg_color = {theme.foreground!r},",
        "        },",
        "        new_tab_hover = {",
        f"            bg_color = {theme.surface!r},",
        f"            fg_color = {theme.text_safe_accent!r},",
        "        },",
        "    },",
        "",
        "    -- Visual indicators (optional)",
        f"    compose_cursor = {theme.warning!r},",
        f"    visual_bell = {theme.warning!r},",
        "}",
        "",
    ]
    return {f"themes/{theme.slug}.lua": "\n".join(lines)}


TARGET = Target(
    id="wezterm",
    target_dir="Terminals/WezTerm",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.lua",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-wezterm.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="WezTerm terminal color schemes (include themes/<slug>.lua)",
)
