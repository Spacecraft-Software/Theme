# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""COSMIC desktop — ``.ron`` colour-scheme renderer.

Renders every Steelbore palette-family theme into a COSMIC
(``com.system76.CosmicTheme``) theme file. The shape follows the
hand-written legacy ``spacecraft-software.ron`` (name, ``is_dark``, accent,
background/container/text/button fields, the three status colours, and the
``panel``/``dock`` component overrides), extended with a small set of
clearly role-mapped fields COSMIC also reads (a high-contrast flag, a focus
/ active-border colour, a link colour, and text-safe colours for the three
status fills) so the theme is complete rather than a minimal port.

Every value is read from the :class:`Theme` through a role accessor — never
a hex literal of its own.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


def _bool(value: bool) -> str:
    return "true" if value else "false"


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.ron`` per theme."""
    lines = [theme.header("COSMIC desktop theme", comment="//").rstrip("\n"), ""]

    lines += [
        "(",
        f'    name: "{theme.name}",',
        f"    is_dark: {_bool(theme.is_dark)},",
        f"    is_high_contrast: {_bool(theme.is_high_contrast)},",
        f'    accent: "{theme.accent}",',
        "",
        "    // Backgrounds — the canvas, then the elevated panel/dock fill.",
        f'    bg_color: "{theme.background}",',
        f'    container_bg_color: "{theme.surface}",',
        "",
        "    // Text — body copy on the canvas and on the container fill; both",
        "    // are the same verified foreground-on-background pairing (§11.0.1).",
        f'    text_color: "{theme.foreground}",',
        f'    container_text_color: "{theme.foreground}",',
        f'    accent_text_color: "{theme.background}",',
        "",
        "    // Buttons — a surface fill with body text, plus the accent button",
        "    // whose fill is the accent and whose text is the canvas (the same",
        "    // pairing measured the other way round, §11.0.1 rule 3).",
        f'    button_bg_color: "{theme.surface}",',
        f'    button_fg_color: "{theme.foreground}",',
        f'    accent_button_bg_color: "{theme.accent}",',
        f'    accent_button_text_color: "{theme.background}",',
        "",
        "    // Links, borders and the active-window focus ring.",
        f'    link_text_color: "{theme.structure}",',
        f'    border_color: "{theme.border}",',
        f'    focus_color: "{theme.focus}",',
        "",
        "    // States. success/destructive fills pair with canvas text — the",
        "    // same allowed inversion as the accent button (§11.0.1 rule 3).",
        "    // warning has no such verified inversion in every palette (the",
        "    // contract permits it only for accent/structure/success/error), so",
        "    // warning carries no paired text colour here.",
        f'    success_color: "{theme.success}",',
        f'    success_text_color: "{theme.background}",',
        f'    warning_color: "{theme.warning}",',
        f'    destructive_color: "{theme.error}",',
        f'    destructive_text_color: "{theme.background}",',
        "",
        "    // Advanced component overrides — panel keeps the canvas, dock",
        "    // steps up to the container fill (the same pairing System76's",
        "    // legacy file used).",
        "    components: {",
        '        "panel": (',
        f'            bg_color: Some("{theme.background}"),',
        "        ),",
        '        "dock": (',
        f'            bg_color: Some("{theme.surface}"),',
        "        ),",
        "    },",
        ")",
        "",
    ]
    return {f"themes/{theme.slug}.ron": "\n".join(lines)}


TARGET = Target(
    id="cosmic",
    target_dir="Desktops/COSMIC",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.ron",),
    archives=(
        Archive(
            path="Desktops/spacecraft-software-cosmic.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
        Archive(
            path="Desktops/spacecraft-software-cosmic-theme.tar.gz",
            fmt="tar.gz",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="COSMIC desktop colour schemes (include themes/<slug>.ron)",
)
