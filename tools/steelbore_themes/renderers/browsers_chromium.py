# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Chromium-family browser themes — one MV3 theme manifest per theme.

One format — a Manifest V3 ``theme`` object, pure JSON, no icons or images
shipped per theme — serves six Spacecraft Software targets that differ only
in vendor directory and product name: Google Chrome, Microsoft Edge, Brave,
Trivalent, Arc and Opera One. ``TARGETS`` is built by a small factory over
that vendor list so the six manifests never drift from one another in shape.

Chrome (and every Chromium fork) installs exactly one theme per unpacked
directory or per ``.zip`` — there is no in-browser theme picker the way an
editor or terminal has one — so each registered hex theme ships as its own
``themes/<slug>/manifest.json`` and its own per-theme archive
(:class:`~steelbore_themes.renderers.Archive` with ``per_theme=True``).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.core import MAINTAINER, PROJECT_URL, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

# Manifest V3 does not expose a light/dark flag — Chrome derives its own
# frame/toolbar chrome purely from the supplied colours, so there is nothing
# for `theme.is_light` to set here (see the module notes returned to the
# reviewer). The colour keys below are otherwise a complete, closest-role
# mapping of every key MV3's `theme.colors` schema documents that a themed
# browser actually paints.


def _render(theme: Theme, product_name: str) -> Mapping[str, str]:
    """One ``themes/<slug>/manifest.json`` — a pure-JSON MV3 theme manifest."""
    payload = {
        "manifest_version": 3,
        "version": "2.0",
        "name": theme.name,
        "description": (
            f"The Spacecraft Software Steelbore palette family for {product_name} "
            f"— {theme.name} ({theme.palette_name} palette)."
        ),
        "author": MAINTAINER,
        "homepage_url": PROJECT_URL,
        "theme": {
            "colors": {
                "frame": list(theme.rgb("background")),
                "frame_inactive": list(theme.rgb("background")),
                "frame_incognito": list(theme.rgb("surface-alt")),
                "frame_incognito_inactive": list(theme.rgb("surface-alt")),
                "toolbar": list(theme.rgb("surface")),
                "toolbar_text": list(theme.rgb("foreground")),
                "tab_text": list(theme.rgb("foreground")),
                "tab_background_text": list(theme.rgb("structure")),
                "tab_background_text_inactive": list(theme.rgb("structure")),
                "bookmark_text": list(theme.rgb("foreground")),
                "ntp_background": list(theme.rgb("background")),
                "ntp_text": list(theme.rgb("foreground")),
                "ntp_link": list(theme.rgb("structure")),
                "ntp_header": list(theme.rgb("surface")),
                "ntp_section": list(theme.rgb("surface")),
                "ntp_section_text": list(theme.rgb("foreground")),
                "ntp_section_link": list(theme.rgb("structure")),
                "button_background": list(theme.rgb("surface")),
                "omnibox_background": list(theme.rgb("surface-alt")),
                "omnibox_text": list(theme.rgb("foreground")),
                "toolbar_button_icon": list(theme.rgb("foreground")),
            },
            "tints": {"buttons": [-1, -1, -1]},
            "properties": {"ntp_background_alignment": "bottom"},
        },
    }
    return {f"themes/{theme.slug}/manifest.json": json.dumps(payload, indent=2) + "\n"}


def _archive(vendor_dir: str) -> Archive:
    """One archive per theme — Chrome's installer takes exactly one theme
    per ``.zip``, so ``{slug}`` is expanded once per registered hex theme."""
    return Archive(
        path=f"Browsers/{vendor_dir}/themes/{vendor_dir}-{{slug}}.zip",
        fmt="zip",
        entries=(("themes/{slug}", ""),),
        per_theme=True,
    )


def _vendor_target(
    vendor_id: str,
    vendor_dir: str,
    product_name: str,
    legacy_extra: tuple[str, ...],
) -> Target:
    return Target(
        id=vendor_id,
        target_dir=f"Browsers/{vendor_dir}",
        render=lambda theme: _render(theme, product_name),
        supports_mono=False,
        legacy_files=("manifest.json", *legacy_extra),
        archives=(_archive(vendor_dir),),
        description=f"{product_name} MV3 theme manifest (themes/<slug>/manifest.json per theme)",
    )


TARGETS = (
    _vendor_target(
        "chrome",
        "spacecraft-software-chrome",
        "Google Chrome",
        (
            "Cached Theme.pak",
            "spacecraft-software-chrome-theme.zip",
            "../spacecraft-software-chrome-theme.zip",
        ),
    ),
    _vendor_target(
        "edge",
        "spacecraft-software-edge",
        "Microsoft Edge",
        (
            "spacecraft-software-edge-theme.zip",
            "../spacecraft-software-edge-theme.zip",
        ),
    ),
    _vendor_target(
        "brave",
        "spacecraft-software-brave",
        "Brave",
        ("spacecraft-software-brave-theme.zip",),
    ),
    _vendor_target(
        "trivalent",
        "spacecraft-software-trivalent",
        "Trivalent",
        ("spacecraft-software-trivalent-theme.zip",),
    ),
    _vendor_target(
        "arc",
        "spacecraft-software-arc",
        "Arc",
        ("spacecraft-software-arc-theme.zip",),
    ),
    _vendor_target(
        "opera_one",
        "spacecraft-software-opera-one",
        "Opera One",
        ("../spacecraft-software-opera-one.zip",),
    ),
)
