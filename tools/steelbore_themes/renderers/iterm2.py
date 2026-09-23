# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""iTerm2 — Apple property-list (``.itermcolors``) colour theme renderer.

``.itermcolors`` is a plist XML document: a flat ``<dict>`` of named colour
entries, each an sRGB triple expressed as ``0.0``-``1.0`` floats.  The format
has no light/dark polarity flag and no ANSI-name (mono) mode, so this renderer
is hex-only (``supports_mono=False``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.core import Theme, hex_to_rgb
from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping


def _float_triple(hex_value: str) -> tuple[float, float, float]:
    """``#RRGGBB`` → ``(r, g, b)`` floats in ``0.0``-``1.0``.

    Unlike :meth:`Theme.rgb_float`, this accepts any hex the theme hands
    back (e.g. ``theme.text_safe_accent``, which already resolves to a role's
    hex rather than a role *name*), not only a role key into ``theme.roles``.
    """
    r, g, b = hex_to_rgb(hex_value)
    return (r / 255.0, g / 255.0, b / 255.0)


def _color_entry(key: str, rgb_float: tuple[float, float, float]) -> list[str]:
    """The plist lines for one named colour entry."""
    r, g, b = rgb_float
    return [
        f"\t<key>{key}</key>",
        "\t<dict>",
        "\t\t<key>Red Component</key>",
        f"\t\t<real>{r:.6f}</real>",
        "\t\t<key>Green Component</key>",
        f"\t\t<real>{g:.6f}</real>",
        "\t\t<key>Blue Component</key>",
        f"\t\t<real>{b:.6f}</real>",
        "\t\t<key>Alpha Component</key>",
        "\t\t<real>1</real>",
        "\t\t<key>Color Space</key>",
        "\t\t<string>sRGB</string>",
        "\t</dict>",
    ]


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.itermcolors`` per theme."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
        theme.header_block("iTerm2 colour theme", "<!--", "-->").rstrip("\n"),
        '<plist version="1.0">',
        "<dict>",
    ]

    # Ansi 0-15 — the only ANSI mapping (§11.1's black/red/green/.../white,
    # bright siblings after); theme.ansi16() is the sole source.
    for index, hex_value in enumerate(theme.ansi16()):
        lines += _color_entry(f"Ansi {index} Color", _float_triple(hex_value))

    lines += _color_entry("Background Color", theme.rgb_float("background"))
    lines += _color_entry("Foreground Color", theme.rgb_float("foreground"))
    # Bold and the active cursor read as body text: foreground, the verified
    # pairing against the canvas.
    lines += _color_entry("Bold Color", theme.rgb_float("foreground"))
    lines += _color_entry("Cursor Color", theme.rgb_float("foreground"))
    # Cursor Text / Selected Text sit on top of a foreground-coloured cursor
    # or a text-safe-accent selection fill — background is the verified
    # inversion pairing for text on those fills (§11's allowed inversion).
    lines += _color_entry("Cursor Text Color", theme.rgb_float("background"))
    lines += _color_entry("Selection Color", _float_triple(theme.text_safe_accent))
    lines += _color_entry("Selected Text Color", theme.rgb_float("background"))
    lines += _color_entry("Link Color", theme.rgb_float("structure"))
    lines += _color_entry("Badge Color", theme.rgb_float("warning"))
    # Cursor Guide is a translucent row highlight — a surface fill, never text.
    lines += _color_entry("Cursor Guide Color", theme.rgb_float("surface"))
    # Tab Color is a non-text swatch (macOS window-tab accent), so the plain
    # accent applies, not the text-safe restriction.
    lines += _color_entry("Tab Color", theme.rgb_float("accent"))

    lines += ["</dict>", "</plist>"]
    return {f"themes/{theme.slug}.itermcolors": "\n".join(lines) + "\n"}


TARGET = Target(
    id="iterm2",
    target_dir="Terminals/iTerm2",
    render=render,
    supports_mono=False,
    legacy_files=("Spacecraft-Software.itermcolors",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-iterm2.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="iTerm2 colour presets (themes/<slug>.itermcolors, plist XML)",
)
