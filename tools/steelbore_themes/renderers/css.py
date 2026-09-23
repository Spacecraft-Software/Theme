# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Plain CSS custom-property tokens — renderer for the ``Steelbore/`` bundle.

Two kinds of output, both hex-only (``supports_mono=False``; ``steelbore-mono``
carries ANSI names, not colours, so it is skipped by the generator):

* ``themes/<slug>.css`` — one self-contained file per theme: a ``:root`` block
  declaring the eleven role tokens plus ``--steelbore-info`` and the §12
  typography tokens, ``color-scheme`` set from the theme's polarity, and a
  minimal ``body`` / ``a`` / ``:focus-visible`` rule set.
* ``steelbore.css`` — the package bundle: the default theme's tokens live
  directly on ``:root``, every theme (default first) repeats them under
  ``[data-theme="<slug>"]``, and a ``prefers-color-scheme: light`` media query
  falls back to whichever theme's slug is ``steelbore-navywhite`` for a reader
  who never sets ``data-theme`` at all.

Every colour is read from the :class:`Theme` passed in; the font names are
literal text (§12), not colours, so they carry no hex.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from steelbore_themes.core import Theme

_FONT_HEADING = "'Share Tech Mono', monospace"
_FONT_BODY = "'Inconsolata', monospace"


def _properties(theme: Theme) -> list[str]:
    """The custom-property lines shared by every ``:root`` / ``[data-theme]`` block."""
    return [
        f"  --steelbore-background: {theme.background};",
        f"  --steelbore-surface: {theme.surface};",
        f"  --steelbore-surface-alt: {theme.surface_alt};",
        f"  --steelbore-foreground: {theme.foreground};",
        f"  --steelbore-accent: {theme.accent};",
        f"  --steelbore-structure: {theme.structure};",
        f"  --steelbore-success: {theme.success};",
        f"  --steelbore-error: {theme.error};",
        f"  --steelbore-warning: {theme.warning};",
        f"  --steelbore-focus: {theme.focus};",
        f"  --steelbore-border: {theme.border};",
        f"  --steelbore-info: {theme.info};",
        f"  --steelbore-font-heading: {_FONT_HEADING};",
        f"  --steelbore-font-body: {_FONT_BODY};",
        f"  color-scheme: {'light' if theme.is_light else 'dark'};",
    ]


def _block(theme: Theme, selector: str) -> list[str]:
    return [f"{selector} {{", *_properties(theme), "}"]


def render(theme: Theme) -> Mapping[str, str]:
    """One self-contained ``themes/<slug>.css`` per theme."""
    lines = [theme.header_block("CSS custom-property theme").rstrip("\n"), ""]
    lines += _block(theme, ":root")
    lines += [
        "",
        "body {",
        "  background: var(--steelbore-background);",
        "  color: var(--steelbore-foreground);",
        "  font-family: var(--steelbore-font-body);",
        "}",
        "",
        "a {",
        "  color: var(--steelbore-structure);",
        "}",
        "",
        ":focus-visible {",
        "  outline: 2px solid var(--steelbore-focus);",
        "}",
        "",
    ]
    return {f"themes/{theme.slug}.css": "\n".join(lines)}


def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
    """``steelbore.css`` — default on ``:root``, every theme under ``[data-theme]``."""
    default = themes[0]
    navywhite = next((t for t in themes if t.slug == "steelbore-navywhite"), None)

    lines = [
        default.header_block("Steelbore palette family — CSS bundle").rstrip("\n"),
        "",
    ]
    lines += _block(default, ":root")
    for theme in themes:
        lines += ["", *_block(theme, f'[data-theme="{theme.slug}"]')]

    if navywhite is not None:
        lines += [
            "",
            "@media (prefers-color-scheme: light) {",
            "  :root:not([data-theme]) {",
        ]
        lines += [f"  {prop}" for prop in _properties(navywhite)]
        lines += ["  }", "}"]

    lines += [""]
    return {"steelbore.css": "\n".join(lines)}


TARGET = Target(
    id="css",
    target_dir="Steelbore",
    render=render,
    supports_mono=False,
    render_bundle=render_bundle,
    legacy_files=("../css",),
    archives=(),
    description="Plain CSS custom-property tokens (themes/<slug>.css, steelbore.css bundle)",
)
