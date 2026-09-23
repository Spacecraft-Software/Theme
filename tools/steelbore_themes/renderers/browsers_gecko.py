# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Gecko (Firefox-family) WebExtension theme manifests.

One MV2 ``theme`` manifest format serves three Spacecraft Software targets
that differ only in vendor id, display name and directory — Firefox, Zen
Browser and Tor Browser, all WebExtension-theme-API-compatible Gecko forks.
Each registered hex theme becomes ``themes/<slug>/manifest.json`` (one
manifest per theme, since an ``.xpi`` holds exactly one manifest at its
root); ``steelbore-mono`` is skipped — ``theme.colors`` is a hex-only field,
so Gecko themes cannot express the 4-bit mono variant.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.core import MAINTAINER, Theme
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

_HOMEPAGE: str = "https://SpacecraftSoftware.org"
_MIN_VERSION: str = "63.0"


def _description(theme: Theme, vendor_display: str) -> str:
    """A one-line ``description`` naming the theme, its conformance and the
    vendor it ships for."""
    if theme.is_fidelity:
        return f"{theme.name} — a non-conforming §11.5 fidelity palette, reproduced verbatim, for {vendor_display}."
    if theme.is_high_contrast:
        return f"{theme.name} — the §11.1.1 high-contrast Spacecraft Software theme for {vendor_display}."
    return f"{theme.name} — a Spacecraft Software Steelbore palette theme for {vendor_display}."


def _colors(theme: Theme) -> dict[str, str]:
    """``theme.colors``: every key mapped to the closest §11.1 role.

    ``toolbar_field_highlight`` is a translucent-looking selection fill in
    most themes, but the format notes are explicit that ``with_alpha`` is not
    valid here — Gecko does not composite this key over content, so it takes
    plain ``accent`` like every other accent fill in this table.
    """
    return {
        "frame": theme.background,
        "frame_inactive": theme.structure,
        "tab_background_text": theme.structure,
        "toolbar": theme.surface,
        "toolbar_text": theme.foreground,
        "toolbar_field": theme.surface_alt,
        "toolbar_field_text": theme.foreground,
        "toolbar_field_border": theme.border,
        "toolbar_field_focus": theme.surface_alt,
        "toolbar_field_border_focus": theme.focus,
        "toolbar_field_highlight": theme.accent,
        "toolbar_field_highlight_text": theme.background,
        "toolbar_top_separator": theme.border,
        "toolbar_bottom_separator": theme.background,
        "tab_line": theme.accent,
        "tab_loading": theme.accent,
        "tab_selected": theme.surface,
        "tab_text": theme.foreground,
        "ntp_background": theme.background,
        "ntp_text": theme.foreground,
        "popup": theme.surface,
        "popup_text": theme.foreground,
        "popup_border": theme.border,
        "popup_highlight": theme.accent,
        "popup_highlight_text": theme.background,
        "sidebar": theme.background,
        "sidebar_text": theme.foreground,
        "sidebar_border": theme.border,
        "sidebar_highlight": theme.accent,
        "sidebar_highlight_text": theme.background,
        "bookmark_text": theme.foreground,
        "button_background_hover": theme.surface,
        "button_background_active": theme.accent,
        "icons": theme.foreground,
        "icons_attention": theme.success,
    }


def _render(theme: Theme, vendor: str, vendor_display: str) -> Mapping[str, str]:
    """One ``themes/<slug>/manifest.json`` for one vendor."""
    manifest: dict[str, object] = {
        "manifest_version": 2,
        "version": "2.0",
        "name": theme.name,
        "description": _description(theme, vendor_display),
        "author": MAINTAINER,
        "developer": {
            "name": MAINTAINER,
            "url": _HOMEPAGE,
        },
        "homepage_url": _HOMEPAGE,
        "browser_specific_settings": {
            "gecko": {
                "id": f"spacecraft-{theme.slug}-{vendor}@SpacecraftSoftware.org",
                "strict_min_version": _MIN_VERSION,
            },
        },
        "theme": {
            "colors": _colors(theme),
            "properties": {
                "color_scheme": "light" if theme.is_light else "dark",
            },
        },
    }
    return {f"themes/{theme.slug}/manifest.json": json.dumps(manifest, indent=2) + "\n"}


def _make_target(vendor: str, vendor_display: str, target_dir: str) -> Target:
    """One :class:`Target` for one Gecko-family vendor directory."""

    def render(theme: Theme) -> Mapping[str, str]:
        return _render(theme, vendor, vendor_display)

    return Target(
        id=vendor,
        target_dir=target_dir,
        render=render,
        supports_mono=False,
        legacy_files=(
            "manifest.json",
            f"spacecraft-software-{vendor}-theme.xpi",
            f"../spacecraft-software-{vendor}-theme.xpi",
        ),
        archives=(
            Archive(
                path=f"{target_dir}/themes/{vendor}-{{slug}}.xpi",
                fmt="xpi",
                entries=(("themes/{slug}", ""),),
                per_theme=True,
            ),
        ),
        description=f"{vendor_display} WebExtension theme manifest (one xpi per theme)",
    )


TARGETS = (
    _make_target("firefox", "Mozilla Firefox", "Browsers/spacecraft-software-firefox"),
    _make_target("zen", "Zen Browser", "Browsers/spacecraft-software-zen"),
    _make_target("tor", "Tor Browser", "Browsers/spacecraft-software-tor"),
)
