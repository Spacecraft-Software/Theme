# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Opera GX mod manifest renderer.

Opera GX mods carry their theme as two HSL colour pairs in
``mod.payload.theme.{dark,light}`` — ``gx_accent`` (the browser chrome accent)
and ``gx_secondary_base`` (the panel/sidebar base colour) — rather than hex.
This module converts the role tokens the mod actually needs, ``accent`` and
``surface``, to ``{h, s, l}`` integers at render time; no hex literal, and no
wallpaper section (per-theme images are not shipped, per ``tools/README.md``
rule 14).

Opera GX has no separate light/dark *reading* of a single palette — each
theme is one fixed set of role colours — so both the ``dark`` and ``light``
payload blocks are filled from the same ``theme.accent`` / ``theme.surface``
pair. That satisfies a light-canvas theme (which should show its own accent
and surface either way) and a dark-canvas theme (which has no separate light
reading to fall back to) with one code path.

Pure JSON gets no ``theme.header()`` (rule 9); ``license.txt`` is a one-line
pointer, also unheadered, alongside it.
"""

from __future__ import annotations

import colorsys
import json
from typing import TYPE_CHECKING

from steelbore_themes.core import MAINTAINER, Theme, hex_to_rgb
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

_LICENSE_POINTER = "GPL-3.0-or-later — see LICENSE at the repository root\n"


def _hex_to_hsl(value: str) -> dict[str, int]:
    """``#RRGGBB`` -> ``{h, s, l}`` integers (``h`` 0-360, ``s``/``l`` 0-100).

    ``colorsys.rgb_to_hls`` returns ``(h, l, s)`` in the ``0.0-1.0`` range;
    reordered and scaled here for the Opera GX mod schema.
    """
    r, g, b = hex_to_rgb(value)
    hue, light, sat = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return {"h": round(hue * 360.0) % 360, "s": round(sat * 100.0), "l": round(light * 100.0)}


def render(theme: Theme) -> Mapping[str, str]:
    """``themes/<slug>/manifest.json`` + ``themes/<slug>/license.txt``."""
    accent_hsl = _hex_to_hsl(theme.accent)
    secondary_hsl = _hex_to_hsl(theme.surface)
    manifest: dict[str, object] = {
        "name": f"Spacecraft Software — {theme.name}",
        "description": (
            f"The Spacecraft Software {theme.name} theme for Opera GX (Steelbore palette family, {theme.palette_name})."
        ),
        "developer": {"name": MAINTAINER},
        "manifest_version": 3,
        "mod": {
            "schema_version": 1,
            "license": "license.txt",
            "payload": {
                "theme": {
                    "dark": {
                        "gx_accent": accent_hsl,
                        "gx_secondary_base": secondary_hsl,
                    },
                    "light": {
                        "gx_accent": accent_hsl,
                        "gx_secondary_base": secondary_hsl,
                    },
                },
            },
        },
        "version": "2.0",
    }
    return {
        f"themes/{theme.slug}/manifest.json": json.dumps(manifest, indent=2) + "\n",
        f"themes/{theme.slug}/license.txt": _LICENSE_POINTER,
    }


TARGET = Target(
    id="opera_gx",
    target_dir="Browsers/spacecraft-software-opera-gx",
    render=render,
    supports_mono=False,
    legacy_files=(
        "manifest.json",
        "../spacecraft-software-opera-gx.zip",
    ),
    archives=(
        Archive(
            path="Browsers/spacecraft-software-opera-gx/themes/spacecraft-software-opera-gx-{slug}.zip",
            fmt="zip",
            entries=(("themes/{slug}", ""),),
            per_theme=True,
        ),
    ),
    description="Opera GX mod manifests (themes/<slug>/manifest.json + license.txt)",
)
