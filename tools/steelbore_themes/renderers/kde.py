# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""KDE Plasma - theme renderer.

Renders Steelbore palette themes into the KDE Plasma colour-scheme INI format
(``.colors``). KDE reads this file's name for display in some versions, so
the target's ``render`` names each output ``themes/<slug>.colors``; the
``Name=`` key inside carries the theme's display name and doubles as the
value ``[General] ColorScheme=`` must repeat.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def _rgb(theme: Theme, role: str) -> str:
    r, g, b = theme.rgb(role)
    return f"{r},{g},{b}"


def _fg_active(theme: Theme) -> str:
    """``ForegroundActive`` — the text-safe accent, since it sits on a fill."""
    return _rgb(theme, "accent" if theme.text_safe_accent == theme.accent else "structure")


def _section(
    theme: Theme,
    *,
    bg_normal: str,
    bg_alt: str,
    fg_normal: str,
    fg_active: str,
) -> list[str]:
    """One ``[Colors:*]``-shaped block of eleven keys, minus the header line.

    ``fg_active`` is the text-safe accent used for ``ForegroundActive``; the
    other foreground slots follow the fixed role mapping the format notes
    specify — structure carries inactive/link/visited/hover, the three
    status roles carry negative/neutral/positive, and focus carries the
    decoration-focus key.
    """
    return [
        f"BackgroundNormal={bg_normal}",
        f"BackgroundAlternate={bg_alt}",
        f"ForegroundNormal={fg_normal}",
        f"ForegroundInactive={_rgb(theme, 'structure')}",
        f"ForegroundActive={fg_active}",
        f"ForegroundLink={_rgb(theme, 'structure')}",
        f"ForegroundVisited={_rgb(theme, 'structure')}",
        f"ForegroundNegative={_rgb(theme, 'error')}",
        f"ForegroundNeutral={_rgb(theme, 'warning')}",
        f"ForegroundPositive={_rgb(theme, 'success')}",
        f"DecorationFocus={_rgb(theme, 'focus')}",
        f"DecorationHover={_rgb(theme, 'structure')}",
    ]


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.colors`` per theme."""
    lines = [theme.header("KDE Plasma colour scheme", comment="#").rstrip("\n"), ""]

    fg_active = _fg_active(theme)

    lines += [
        "[General]",
        f"ColorScheme={theme.name}",
        f"Name={theme.name}",
        "shadeSortColumn=true",
        "",
        "[KDE]",
        "contrast=7",
        "",
        "[WM]",
        f"activeBackground={_rgb(theme, 'background')}",
        f"activeBlend={_rgb(theme, 'background')}",
        f"activeForeground={_rgb(theme, 'foreground')}",
        f"inactiveBackground={_rgb(theme, 'surface')}",
        f"inactiveBlend={_rgb(theme, 'surface')}",
        f"inactiveForeground={_rgb(theme, 'structure')}",
        "",
    ]

    # [Colors:Window] - main window chrome: canvas / surface, body text.
    lines += ["[Colors:Window]"]
    lines += _section(
        theme,
        bg_normal=_rgb(theme, "background"),
        bg_alt=_rgb(theme, "surface"),
        fg_normal=_rgb(theme, "foreground"),
        fg_active=fg_active,
    )
    lines.append("")

    # [Colors:View] - list/text views sit on the alternate surface.
    lines += ["[Colors:View]"]
    lines += _section(
        theme,
        bg_normal=_rgb(theme, "surface-alt"),
        bg_alt=_rgb(theme, "background"),
        fg_normal=_rgb(theme, "foreground"),
        fg_active=fg_active,
    )
    lines.append("")

    # [Colors:Button] - buttons: surface fill, body text.
    lines += ["[Colors:Button]"]
    lines += _section(
        theme,
        bg_normal=_rgb(theme, "surface"),
        bg_alt=_rgb(theme, "background"),
        fg_normal=_rgb(theme, "foreground"),
        fg_active=fg_active,
    )
    lines.append("")

    # [Colors:Selection] - accent fill; text is the canvas on top of it, the
    # same verified pairing measured the other way round.
    lines += ["[Colors:Selection]"]
    lines += [
        f"BackgroundNormal={_rgb(theme, 'accent')}",
        f"BackgroundAlternate={_rgb(theme, 'focus')}",
        f"ForegroundNormal={_rgb(theme, 'background')}",
        f"ForegroundInactive={_rgb(theme, 'foreground')}",
        f"ForegroundLink={_rgb(theme, 'background')}",
        f"ForegroundVisited={_rgb(theme, 'background')}",
        f"ForegroundNegative={_rgb(theme, 'error')}",
        f"ForegroundNeutral={_rgb(theme, 'warning')}",
        f"ForegroundPositive={_rgb(theme, 'success')}",
        f"DecorationFocus={_rgb(theme, 'focus')}",
        f"DecorationHover={_rgb(theme, 'structure')}",
        "",
    ]

    # [Colors:Tooltip] - surface fill, body text.
    lines += ["[Colors:Tooltip]"]
    lines += _section(
        theme,
        bg_normal=_rgb(theme, "surface"),
        bg_alt=_rgb(theme, "surface-alt"),
        fg_normal=_rgb(theme, "foreground"),
        fg_active=fg_active,
    )
    lines.append("")

    # [Colors:Complementary] - the alternate surface, standing in for a
    # secondary panel band (KDE's "complementary" colour set).
    lines += ["[Colors:Complementary]"]
    lines += _section(
        theme,
        bg_normal=_rgb(theme, "surface-alt"),
        bg_alt=_rgb(theme, "surface"),
        fg_normal=_rgb(theme, "foreground"),
        fg_active=fg_active,
    )
    lines.append("")

    # [Colors:Header] - panel/header bars: surface fill, body text.
    lines += ["[Colors:Header]"]
    lines += _section(
        theme,
        bg_normal=_rgb(theme, "surface"),
        bg_alt=_rgb(theme, "background"),
        fg_normal=_rgb(theme, "foreground"),
        fg_active=fg_active,
    )
    lines.append("")

    return {f"themes/{theme.slug}.colors": "\n".join(lines)}


TARGET = Target(
    id="kde",
    target_dir="Desktops/KDE_Plasma",
    render=render,
    supports_mono=False,
    legacy_files=("Spacecraft-Software.colors",),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-kde_plasma.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-kde-plasma-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="KDE Plasma colour schemes (include themes/<slug>.colors)",
)
