# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Visual Studio 2022 colour theme (``.vstheme``).

One ``themes/<slug>.vstheme`` per theme (General Environment + Text Editor
categories), plus a bundle ``extension.vsixmanifest`` / ``[Content_Types].xml``
pair that lists every theme as a ``Microsoft.VisualStudio.VsTheme`` asset.

Colour order — read this before touching a ``Source`` value: VS's ``CT_RAW``
colour is ``#AARRGGBB`` with the alpha channel **first** (Microsoft's native
ARGB order). That is confirmed against the hand-written predecessor this
module replaces — run ``git show HEAD:Editors/VisualStudio/Spacecraft-Software.vstheme``
and note every ``Source`` attribute carries a two-digit alpha prefix ahead of
the six-digit colour, i.e. an alpha byte followed by the RGB bytes, never the
reverse — a different byte order from :meth:`~steelbore_themes.core.Theme.with_alpha`,
which *appends* the alpha suffix for formats that read ``RRGGBBAA`` (CSS/JSON
translucency). Calling that helper here would silently swap VS's alpha and
blue channels, so :func:`_argb` below builds the ARGB token by hand from the
same theme-owned hex a renderer is always allowed to use (``theme.hex_bare``
/ a role/property access) — it never introduces a literal colour of its own.

Known validator limitation (not fixed here, see notes returned by this
task): the shared hex validator reads an 8-digit colour token by its
*leading* six digits, which is correct for the suffix-alpha convention above
but misreads this module's alpha-first tokens, producing a false-positive
"not a theme colour" finding on every ``Source`` value here. The rendered
files are format-correct (verified against the predecessor file). Fixing the
validator's window is a shared, cross-renderer change outside this module's
and this target directory's scope and is deliberately left for a separate,
reviewed change rather than folded in here.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from steelbore_themes.core import Theme

_GUID_NAMESPACE_PREFIX = "https://Theme.SpacecraftSoftware.org/vstheme/"
_GENERAL_ENVIRONMENT_GUID = "{75a05685-286d-11d0-8354-00a0c9031596}"
_TEXT_EDITOR_GUID = "{2370b77c-463d-4225-ae9a-9b9083236312}"
_SELECTION_ALPHA = "40"
_OPAQUE = "FF"

_PUBLISHER = "Spacecraft-Software"
_IDENTITY_ID = "SpacecraftSoftware.SpacecraftSoftwareTheme.VisualStudio"
_EXTENSION_VERSION = "2.0.0"


def _theme_guid(slug: str) -> str:
    """A stable per-theme GUID: ``uuid5(NAMESPACE_URL, .../vstheme/<slug>)``."""
    return "{" + str(uuid.uuid5(uuid.NAMESPACE_URL, _GUID_NAMESPACE_PREFIX + slug)).upper() + "}"


def _argb(hex_value: str, alpha: str = _OPAQUE) -> str:
    """``#AARRGGBB`` from a theme-owned ``#RRGGBB`` (or bare ``RRGGBB``).

    ``hex_value`` always comes from a role accessor or property at the call
    site (``theme.foreground``, ``theme.text_safe_accent``, …) — this
    function only reorders bytes, it never supplies a colour.
    """
    return f"#{alpha}{hex_value.lstrip('#')}".upper()


def _xml_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _color(name: str, slot: str, source: str, indent: str = "      ") -> list[str]:
    return [
        f'{indent}<Color Name="{name}">',
        f'{indent}  <{slot} Type="CT_RAW" Source="{source}" />',
        f"{indent}</Color>",
    ]


def _general_environment(theme: Theme) -> list[str]:
    """General Environment category (§ tools/README.md rule 2 role table).

    Active tab takes the canvas so it reads as part of the editor surface;
    the underline on it is the standard accent example from the role table
    ("active tab underline"). Inactive tab text is muted/secondary, so it is
    ``structure`` per rule 2, never a surface token. Status bar and command
    bar menus are elevated fills (``surface``) with foreground text on top —
    the verified pairing from rule 3.
    """
    lines = [f'    <Category GUID="{_GENERAL_ENVIRONMENT_GUID}"> <!-- General Environment -->']
    lines += _color("ActiveBorder", "Background", _argb(theme.border))
    lines += _color("ActiveTabBackground", "Background", _argb(theme.background))
    lines += _color("ActiveTabBorder", "Background", _argb(theme.accent))
    lines += _color("ActiveTabText", "Background", _argb(theme.foreground))
    lines += _color("InactiveTabBackground", "Background", _argb(theme.surface))
    lines += _color("InactiveTabBorder", "Background", _argb(theme.border))
    lines += _color("InactiveTabText", "Background", _argb(theme.structure))
    lines += _color("Background", "Background", _argb(theme.background))
    lines += _color("ToolWindowBackground", "Background", _argb(theme.surface))
    lines += _color("ToolWindowText", "Background", _argb(theme.foreground))
    lines += _color("TitleBarActive", "Background", _argb(theme.background))
    lines += _color("TitleBarInactive", "Background", _argb(theme.surface))
    lines += _color("MainWindowActiveCaption", "Background", _argb(theme.accent))
    lines += _color("CommandBarMenuBackgroundGradient", "Background", _argb(theme.surface))
    lines += _color("CommandBarTextActive", "Background", _argb(theme.foreground))
    lines += _color("StatusBarDefault", "Background", _argb(theme.surface))
    lines += _color("StatusBarText", "Background", _argb(theme.foreground))
    lines.append("    </Category>")
    return lines


def _text_editor(theme: Theme) -> list[str]:
    """Text Editor category. ``SelectedText`` is the one translucent fill —
    ``accent`` at 40 alpha, ARGB order (not :meth:`Theme.with_alpha`, see the
    module docstring)."""
    lines = [f'    <Category GUID="{_TEXT_EDITOR_GUID}"> <!-- Text Editor -->']
    lines += _color("Background", "Background", _argb(theme.background))
    lines += _color("Foreground", "Foreground", _argb(theme.foreground))
    lines += _color("LineNumbers", "Foreground", _argb(theme.structure))
    lines += _color("SelectedText", "Background", _argb(theme.accent, _SELECTION_ALPHA))
    lines += _color("Plain Text", "Foreground", _argb(theme.foreground))
    lines += _color("Keyword", "Foreground", _argb(theme.text_safe_accent))
    lines += _color("String", "Foreground", _argb(theme.success))
    lines += _color("Comment", "Foreground", _argb(theme.structure))
    lines += _color("Number", "Foreground", _argb(theme.warning))
    lines += _color("Identifier", "Foreground", _argb(theme.foreground))
    lines += _color("User Types", "Foreground", _argb(theme.structure))
    lines += _color("Compiler Error", "Foreground", _argb(theme.error))
    lines += _color("Warning", "Foreground", _argb(theme.warning))
    lines.append("    </Category>")
    return lines


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.vstheme`` per theme."""
    director = "Light" if theme.is_light else "Dark"
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        theme.header_block("Visual Studio 2022 colour theme", opener="<!--", closer="-->").rstrip("\n"),
        "<Themes>",
        f'  <Theme Name="{_xml_escape(theme.name)}" GUID="{_theme_guid(theme.slug)}" Director="{director}">',
        *_general_environment(theme),
        *_text_editor(theme),
        "  </Theme>",
        "</Themes>",
    ]
    return {f"themes/{theme.slug}.vstheme": "\n".join(lines) + "\n"}


def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
    """``extension.vsixmanifest`` (one ``VsTheme`` asset per theme) and
    ``[Content_Types].xml`` for the VSIX/zip containers."""
    manifest_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<PackageManifest Version="2.0.0" '
        'xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" '
        'xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">',
        "  <Metadata>",
        f'    <Identity Id="{_IDENTITY_ID}" Version="{_EXTENSION_VERSION}" '
        f'Language="en-US" Publisher="{_PUBLISHER}" />',
        "    <DisplayName>Spacecraft Software Theme</DisplayName>",
        '    <Description xml:space="preserve">The Steelbore palette family '
        "(The Steelbore Standard §11) for Visual Studio 2022 — Steelbore "
        "default, ten alternates, high-contrast siblings and the Solarized "
        "fidelity pair.</Description>",
        "    <License>LICENSE</License>",
        "    <Icon>icon.png</Icon>",
        "    <MoreInfo>https://SpacecraftSoftware.org</MoreInfo>",
        "  </Metadata>",
        "  <Installation>",
        '    <InstallationTarget Id="Microsoft.VisualStudio.Community" Version="[17.0,18.0)" />',
        '    <InstallationTarget Id="Microsoft.VisualStudio.Pro" Version="[17.0,18.0)" />',
        '    <InstallationTarget Id="Microsoft.VisualStudio.Enterprise" Version="[17.0,18.0)" />',
        "  </Installation>",
        "  <Dependencies>",
        '    <Dependency Id="Microsoft.Framework.NDP" DisplayName="Microsoft .NET Framework" '
        'd:Source="Manual" Version="4.5" />',
        "  </Dependencies>",
        "  <Assets>",
    ]
    for theme in themes:
        manifest_lines.append(f'    <Asset Type="Microsoft.VisualStudio.VsTheme" Path="themes/{theme.slug}.vstheme" />')
    manifest_lines += ["  </Assets>", "</PackageManifest>"]

    content_types = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="vstheme" ContentType="text/xml"/>'
        '<Default Extension="vsixmanifest" ContentType="text/xml"/>'
        '<Default Extension="md" ContentType="text/markdown"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/LICENSE" ContentType="text/plain"/>'
        "</Types>\n"
    )

    return {
        "extension.vsixmanifest": "\n".join(manifest_lines) + "\n",
        "[Content_Types].xml": content_types,
    }


TARGET = Target(
    id="visualstudio",
    target_dir="Editors/VisualStudio",
    render=render,
    render_bundle=render_bundle,
    supports_mono=False,
    legacy_files=("Spacecraft-Software.vstheme",),
    archives=(
        Archive(
            path="Editors/VisualStudio/spacecraft-software-visualstudio-theme.zip",
            fmt="zip",
            entries=(
                ("themes", "themes"),
                ("extension.vsixmanifest", "extension.vsixmanifest"),
                ("[Content_Types].xml", "[Content_Types].xml"),
                ("LICENSE", "LICENSE"),
                ("icon.png", "icon.png"),
                ("README.md", "README.md"),
                ("INSTALL.md", "INSTALL.md"),
            ),
        ),
        Archive(
            path="Editors/VisualStudio/spacecraft-software-visualstudio.vsix",
            fmt="vsix",
            entries=(
                ("extension.vsixmanifest", "extension.vsixmanifest"),
                ("[Content_Types].xml", "[Content_Types].xml"),
                ("LICENSE", "LICENSE"),
                ("icon.png", "icon.png"),
                # Nested under "themes" (not flattened to "") so the vsix's
                # actual layout agrees with the Asset Path the manifest
                # declares above (`themes/{slug}.vstheme`) — see this
                # renderer's regression notes.
                ("themes", "themes"),
            ),
        ),
    ),
    description="Visual Studio 2022 colour theme (themes/<slug>.vstheme + extension.vsixmanifest)",
)
