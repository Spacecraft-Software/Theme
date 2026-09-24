# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""VS Code and Google Antigravity colour themes.

One render function serves both vendor directories — Antigravity is a VS Code
fork and consumes the identical theme JSON and `package.json` shape. A small
factory builds the two :class:`~steelbore_themes.renderers.Target` objects
with different ids, directories, package identities and archives; each also
emits the `.vsix` container manifest pair and a `.vsix` archive.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from steelbore_themes.core import ROLES, Theme
from steelbore_themes.renderers import Archive, BundleFn, Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

_ALPHA_SOFT = "14"
_ALPHA_MED = "26"
_ALPHA_STRONG = "40"
_ALPHA_HOVER = "CC"


def _vscode_type(theme: Theme) -> str:
    """VS Code's ``type``: ``dark`` | ``light`` | ``hc`` | ``hcLight``."""
    if theme.is_high_contrast:
        return "hcLight" if theme.is_light else "hc"
    return "light" if theme.is_light else "dark"


def _ui_theme(theme: Theme) -> str:
    """The `contributes.themes[].uiTheme` value matching :func:`_vscode_type`."""
    return {
        "dark": "vs-dark",
        "light": "vs",
        "hc": "hc-black",
        "hcLight": "hc-light",
    }[_vscode_type(theme)]


def _colors(theme: Theme) -> dict[str, str]:
    """The workbench `colors` map — every key a §11.1 role token."""
    ansi = theme.ansi
    bright = theme.ansi_bright
    return {
        # Editor surface and text
        "editor.background": theme.background,
        "editor.foreground": theme.foreground,
        "editorLineNumber.foreground": theme.structure,
        "editorLineNumber.activeForeground": theme.foreground,
        "editorCursor.foreground": theme.focus,
        "editorCursor.background": theme.background,
        "editor.selectionBackground": theme.with_alpha("accent", _ALPHA_STRONG),
        "editor.inactiveSelectionBackground": theme.with_alpha("accent", _ALPHA_SOFT),
        "editor.selectionHighlightBackground": theme.with_alpha("success", _ALPHA_SOFT),
        "editor.wordHighlightBackground": theme.with_alpha("structure", _ALPHA_SOFT),
        "editor.wordHighlightStrongBackground": theme.with_alpha("structure", _ALPHA_MED),
        "editor.findMatchBackground": theme.with_alpha("warning", _ALPHA_MED),
        "editor.findMatchHighlightBackground": theme.with_alpha("warning", _ALPHA_SOFT),
        "editor.lineHighlightBackground": theme.surface,
        "editorIndentGuide.background1": theme.with_alpha("structure", _ALPHA_SOFT),
        "editorIndentGuide.activeBackground1": theme.with_alpha("structure", _ALPHA_MED),
        "editorWhitespace.foreground": theme.with_alpha("structure", _ALPHA_MED),
        "editorBracketMatch.background": theme.with_alpha("focus", _ALPHA_SOFT),
        "editorBracketMatch.border": theme.focus,
        "editorRuler.foreground": theme.with_alpha("structure", _ALPHA_SOFT),
        "editorCodeLens.foreground": theme.structure,
        "editorLink.activeForeground": theme.focus,
        "editor.foldBackground": theme.with_alpha("structure", _ALPHA_SOFT),
        # Gutter
        "editorGutter.background": theme.background,
        "editorGutter.modifiedBackground": theme.warning,
        "editorGutter.addedBackground": theme.success,
        "editorGutter.deletedBackground": theme.error,
        "editorGutter.foldingControlForeground": theme.structure,
        # Widgets
        "editorWidget.background": theme.surface,
        "editorWidget.foreground": theme.foreground,
        "editorWidget.border": theme.border,
        "editorWidget.resizeBorder": theme.focus,
        "editorSuggestWidget.background": theme.surface,
        "editorSuggestWidget.border": theme.border,
        "editorSuggestWidget.foreground": theme.foreground,
        "editorSuggestWidget.selectedBackground": theme.with_alpha("accent", _ALPHA_MED),
        "editorSuggestWidget.selectedForeground": theme.foreground,
        "editorSuggestWidget.highlightForeground": theme.text_safe_accent,
        "editorHoverWidget.background": theme.surface,
        "editorHoverWidget.border": theme.border,
        "editorHoverWidget.foreground": theme.foreground,
        # Diagnostics
        "editorError.foreground": theme.error,
        "editorError.border": theme.with_alpha("error", _ALPHA_SOFT),
        "editorWarning.foreground": theme.warning,
        "editorWarning.border": theme.with_alpha("warning", _ALPHA_SOFT),
        "editorInfo.foreground": theme.info,
        # Diff editor
        "diffEditor.insertedTextBackground": theme.with_alpha("success", _ALPHA_MED),
        "diffEditor.removedTextBackground": theme.with_alpha("error", _ALPHA_MED),
        "diffEditor.insertedLineBackground": theme.with_alpha("success", _ALPHA_SOFT),
        "diffEditor.removedLineBackground": theme.with_alpha("error", _ALPHA_SOFT),
        "diffEditor.diagonalFill": theme.with_alpha("structure", _ALPHA_SOFT),
        "diffEditor.border": theme.border,
        # Activity bar
        "activityBar.background": theme.background,
        "activityBar.foreground": theme.foreground,
        "activityBar.inactiveForeground": theme.structure,
        "activityBar.border": theme.border,
        "activityBarBadge.background": theme.accent,
        "activityBarBadge.foreground": theme.background,
        # Side bar
        "sideBar.background": theme.surface,
        "sideBar.foreground": theme.foreground,
        "sideBar.border": theme.border,
        "sideBarTitle.foreground": theme.foreground,
        "sideBarSectionHeader.background": theme.surface_alt,
        "sideBarSectionHeader.foreground": theme.foreground,
        "sideBarSectionHeader.border": theme.border,
        # Lists and trees
        "list.activeSelectionBackground": theme.with_alpha("accent", _ALPHA_MED),
        "list.activeSelectionForeground": theme.foreground,
        "list.inactiveSelectionBackground": theme.with_alpha("structure", _ALPHA_SOFT),
        "list.inactiveSelectionForeground": theme.foreground,
        "list.hoverBackground": theme.with_alpha("structure", _ALPHA_SOFT),
        "list.hoverForeground": theme.foreground,
        "list.focusBackground": theme.with_alpha("focus", _ALPHA_SOFT),
        "list.focusForeground": theme.foreground,
        "list.highlightForeground": theme.text_safe_accent,
        "list.errorForeground": theme.error,
        "list.warningForeground": theme.warning,
        "list.dropBackground": theme.with_alpha("accent", _ALPHA_MED),
        "tree.indentGuidesStroke": theme.structure,
        # Tabs
        "tab.activeBackground": theme.background,
        "tab.activeForeground": theme.foreground,
        "tab.inactiveBackground": theme.surface,
        # foreground (not structure): structure-on-surface is <4.5:1 on some
        # palettes (§11.1.1 large-text-or-ui-only) and this is normal-size text
        "tab.inactiveForeground": theme.foreground,
        "tab.activeBorderTop": theme.accent,
        "tab.border": theme.border,
        "tab.hoverBackground": theme.with_alpha("structure", _ALPHA_SOFT),
        "tab.unfocusedActiveForeground": theme.foreground,
        "editorGroupHeader.tabsBackground": theme.surface,
        "editorGroupHeader.tabsBorder": theme.border,
        "editorGroup.border": theme.border,
        # Status bar
        "statusBar.background": theme.surface,
        "statusBar.foreground": theme.foreground,
        "statusBar.border": theme.border,
        "statusBar.noFolderBackground": theme.surface_alt,
        # error (not warning): rule 3's safe inversion list is
        # accent/structure/success/error only — warning-vs-background
        # contrast is not guaranteed >=4.5:1 across the family (solarized
        # light measures 2.98:1), so the debugging state borrows the
        # alarming/attention-grabbing `error` fill instead.
        "statusBar.debuggingBackground": theme.error,
        "statusBar.debuggingForeground": theme.background,
        "statusBarItem.hoverBackground": theme.with_alpha("accent", _ALPHA_SOFT),
        "statusBarItem.remoteBackground": theme.accent,
        "statusBarItem.remoteForeground": theme.background,
        # Title bar
        "titleBar.activeBackground": theme.background,
        "titleBar.activeForeground": theme.foreground,
        "titleBar.inactiveBackground": theme.surface,
        # foreground (not structure): structure-on-surface is <4.5:1 on some
        # palettes (§11.1.1 large-text-or-ui-only) and this is normal-size text
        "titleBar.inactiveForeground": theme.foreground,
        "titleBar.border": theme.border,
        # Panel
        "panel.background": theme.surface,
        "panel.border": theme.border,
        "panelTitle.activeForeground": theme.foreground,
        "panelTitle.activeBorder": theme.accent,
        # foreground (not structure): structure-on-surface is <4.5:1 on some
        # palettes (§11.1.1 large-text-or-ui-only) and this is normal-size text
        "panelTitle.inactiveForeground": theme.foreground,
        # Terminal
        "terminal.background": theme.surface_alt,
        "terminal.foreground": theme.foreground,
        "terminal.cursorForeground": theme.focus,
        "terminal.selectionBackground": theme.with_alpha("accent", _ALPHA_MED),
        "terminal.ansiBlack": ansi["black"],
        "terminal.ansiRed": ansi["red"],
        "terminal.ansiGreen": ansi["green"],
        "terminal.ansiYellow": ansi["yellow"],
        "terminal.ansiBlue": ansi["blue"],
        "terminal.ansiMagenta": ansi["magenta"],
        "terminal.ansiCyan": ansi["cyan"],
        "terminal.ansiWhite": ansi["white"],
        "terminal.ansiBrightBlack": bright["black"],
        "terminal.ansiBrightRed": bright["red"],
        "terminal.ansiBrightGreen": bright["green"],
        "terminal.ansiBrightYellow": bright["yellow"],
        "terminal.ansiBrightBlue": bright["blue"],
        "terminal.ansiBrightMagenta": bright["magenta"],
        "terminal.ansiBrightCyan": bright["cyan"],
        "terminal.ansiBrightWhite": bright["white"],
        # Focus
        "focusBorder": theme.focus,
        # Inputs
        "input.background": theme.surface_alt,
        "input.foreground": theme.foreground,
        "input.border": theme.border,
        "input.placeholderForeground": theme.structure,
        "inputOption.activeBorder": theme.focus,
        "inputValidation.errorBackground": theme.with_alpha("error", _ALPHA_SOFT),
        "inputValidation.errorBorder": theme.error,
        "inputValidation.warningBackground": theme.with_alpha("warning", _ALPHA_SOFT),
        "inputValidation.warningBorder": theme.warning,
        # Dropdown
        "dropdown.background": theme.surface_alt,
        "dropdown.foreground": theme.foreground,
        "dropdown.border": theme.border,
        # Buttons
        "button.background": theme.accent,
        "button.foreground": theme.background,
        "button.hoverBackground": theme.with_alpha("accent", _ALPHA_HOVER),
        "button.secondaryBackground": theme.surface,
        "button.secondaryForeground": theme.foreground,
        # Badge / progress
        "badge.background": theme.accent,
        "badge.foreground": theme.background,
        "progressBar.background": theme.accent,
        # Notifications
        "notifications.background": theme.surface,
        "notifications.foreground": theme.foreground,
        "notifications.border": theme.border,
        "notificationCenterHeader.background": theme.surface_alt,
        "notificationCenterHeader.foreground": theme.foreground,
        "notificationsErrorIcon.foreground": theme.error,
        "notificationsWarningIcon.foreground": theme.warning,
        "notificationsInfoIcon.foreground": theme.info,
        # Peek view
        "peekView.border": theme.accent,
        "peekViewEditor.background": theme.surface_alt,
        "peekViewResult.background": theme.surface,
        "peekViewResult.foreground": theme.foreground,
        "peekViewResult.selectionBackground": theme.with_alpha("accent", _ALPHA_MED),
        "peekViewTitle.background": theme.surface,
        "peekViewTitleLabel.foreground": theme.foreground,
        # foreground (not structure): structure-on-surface is <4.5:1 on some
        # palettes (§11.1.1 large-text-or-ui-only) and this is normal-size text
        "peekViewTitleDescription.foreground": theme.foreground,
        # Git decorations
        "gitDecoration.addedResourceForeground": theme.success,
        "gitDecoration.modifiedResourceForeground": theme.warning,
        "gitDecoration.deletedResourceForeground": theme.error,
        "gitDecoration.untrackedResourceForeground": theme.success,
        "gitDecoration.ignoredResourceForeground": theme.structure,
        "gitDecoration.conflictingResourceForeground": theme.error,
        # Minimap
        "minimap.background": theme.surface_alt,
        "minimap.selectionHighlight": theme.with_alpha("accent", _ALPHA_MED),
        "minimap.errorHighlight": theme.error,
        "minimap.warningHighlight": theme.warning,
        "minimapGutter.addedBackground": theme.success,
        "minimapGutter.modifiedBackground": theme.warning,
        "minimapGutter.deletedBackground": theme.error,
        # Scrollbar
        "scrollbarSlider.background": theme.with_alpha("structure", _ALPHA_SOFT),
        "scrollbarSlider.hoverBackground": theme.with_alpha("structure", _ALPHA_MED),
        "scrollbarSlider.activeBackground": theme.with_alpha("structure", _ALPHA_STRONG),
        # Breadcrumbs
        "breadcrumb.foreground": theme.structure,
        "breadcrumb.focusForeground": theme.foreground,
        "breadcrumb.activeSelectionForeground": theme.text_safe_accent,
        "breadcrumbPicker.background": theme.surface,
        # Menus
        "menu.background": theme.surface,
        "menu.foreground": theme.foreground,
        "menu.border": theme.border,
        "menu.selectionBackground": theme.with_alpha("accent", _ALPHA_MED),
        "menu.selectionForeground": theme.foreground,
        "menu.separatorBackground": theme.border,
        "menubar.selectionBackground": theme.with_alpha("accent", _ALPHA_SOFT),
        # Quick input
        "quickInput.background": theme.surface,
        "quickInput.foreground": theme.foreground,
        "quickInputList.focusBackground": theme.with_alpha("accent", _ALPHA_MED),
        "quickInputList.focusForeground": theme.foreground,
        # Links
        "textLink.foreground": theme.structure,
        "textLink.activeForeground": theme.focus,
        # Picker group
        "pickerGroup.border": theme.border,
        # foreground (not structure): structure-on-surface is <4.5:1 on some
        # palettes (§11.1.1 large-text-or-ui-only) and this is normal-size text
        "pickerGroup.foreground": theme.foreground,
    }


def _token_colors(theme: Theme) -> list[dict[str, object]]:
    """TextMate `tokenColors` — role mapping fixed by the task brief."""
    return [
        {
            "scope": ["comment", "punctuation.definition.comment"],
            "settings": {"foreground": theme.structure, "fontStyle": "italic"},
        },
        {
            "scope": ["keyword", "storage.type", "storage.modifier"],
            "settings": {"foreground": theme.text_safe_accent, "fontStyle": "bold"},
        },
        {
            "scope": ["string", "string.template"],
            "settings": {"foreground": theme.success},
        },
        {
            "scope": ["entity.name.function", "support.function"],
            "settings": {"foreground": theme.focus},
        },
        {
            "scope": ["entity.name.type", "entity.name.class", "support.type"],
            "settings": {"foreground": theme.structure},
        },
        {
            "scope": ["variable", "meta.definition.variable"],
            "settings": {"foreground": theme.foreground},
        },
        {
            "scope": ["constant.numeric", "constant.language"],
            "settings": {"foreground": theme.warning},
        },
        {
            "scope": ["entity.name.tag", "markup.heading"],
            "settings": {"foreground": theme.error},
        },
        {
            "scope": ["keyword.operator", "punctuation"],
            "settings": {"foreground": theme.foreground},
        },
        {
            "scope": ["invalid", "invalid.illegal"],
            "settings": {"foreground": theme.error, "fontStyle": "underline"},
        },
        {
            "scope": ["markup.inserted"],
            "settings": {"foreground": theme.success},
        },
        {
            "scope": ["markup.deleted"],
            "settings": {"foreground": theme.error},
        },
        {
            "scope": ["markup.changed"],
            "settings": {"foreground": theme.warning},
        },
    ]


def _semantic_token_colors(theme: Theme) -> dict[str, object]:
    """`semanticTokenColors` — the same role mapping as :func:`_token_colors`."""
    return {
        "comment": {"foreground": theme.structure, "fontStyle": "italic"},
        "keyword": {"foreground": theme.text_safe_accent, "fontStyle": "bold"},
        "string": {"foreground": theme.success},
        "function": {"foreground": theme.focus},
        "method": {"foreground": theme.focus},
        "class": {"foreground": theme.structure},
        "type": {"foreground": theme.structure},
        "interface": {"foreground": theme.structure},
        "number": {"foreground": theme.warning},
        "variable": {"foreground": theme.foreground},
        "parameter": {"foreground": theme.foreground},
        "property": {"foreground": theme.foreground},
        "namespace": {"foreground": theme.structure},
        "operator": {"foreground": theme.foreground},
        "punctuation": {"foreground": theme.foreground},
    }


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.json`` per theme — shared by VS Code and Antigravity."""
    payload = {
        "name": theme.name,
        "type": _vscode_type(theme),
        "semanticHighlighting": True,
        "colors": _colors(theme),
        "tokenColors": _token_colors(theme),
        "semanticTokenColors": _semantic_token_colors(theme),
    }
    return {f"themes/{theme.slug}.json": json.dumps(payload, indent=2) + "\n"}


@dataclass(frozen=True, slots=True)
class _PackageMeta:
    """Per-vendor `package.json` / README identity."""

    name: str
    display_name: str
    description: str
    homepage: str
    ship_vsix: bool


def _role_table_md(theme: Theme) -> str:
    """A short Markdown table of the default palette's 11 roles."""
    lines = ["| Role | Hex |", "| --- | --- |"]
    for role in ROLES:
        label = role.replace("-", " ").title()
        lines.append(f"| {label} | `{theme.roles[role]}` |")
    return "\n".join(lines)


def _slug_table_md(themes: Sequence[Theme]) -> str:
    lines = ["| Slug | Name | Type |", "| --- | --- | --- |"]
    for theme in themes:
        lines.append(f"| `{theme.slug}` | {theme.name} | {_vscode_type(theme)} |")
    return "\n".join(lines)


def _make_render_bundle(meta: _PackageMeta) -> BundleFn:
    def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
        default_theme = themes[0]
        contributes_themes = [
            {
                "label": theme.name,
                "uiTheme": _ui_theme(theme),
                "path": f"./themes/{theme.slug}.json",
            }
            for theme in themes
        ]
        package = {
            "name": meta.name,
            "displayName": meta.display_name,
            "description": meta.description,
            "version": "2.0.0",
            "publisher": "Spacecraft-Software",
            "author": "Mohamed Hammad",
            "license": "GPL-3.0-or-later",
            "icon": "icon.png",
            "repository": {
                "type": "git",
                "url": "https://github.com/Spacecraft-Software/Theme",
            },
            "bugs": {"url": "https://github.com/Spacecraft-Software/Theme/issues"},
            "homepage": meta.homepage,
            "engines": {"vscode": "^1.60.0"},
            "categories": ["Themes"],
            "contributes": {"themes": contributes_themes},
        }

        readme_lines = [
            f"# {meta.display_name}",
            "",
            meta.description,
            "",
            "## The Steelbore palette family",
            "",
            f"This package ships the full Steelbore palette family (The Steelbore "
            f"Standard §11) as {len(themes)} VS Code-compatible colour themes — one "
            "JSON file per theme, generated from the canonical `steelbore.toml` "
            "contract. "
            f"**{default_theme.name}** (`{default_theme.slug}`) is the default; "
            "every palette also ships a `-high-contrast` sibling for §18.1 "
            "accessible mode, each measured at 7:1 or better against its own "
            "canvas.",
            "",
            "`solarized-dark` and `solarized-light` are §11.5 **fidelity "
            "palettes** — reproduced verbatim from upstream Solarized for "
            "interoperability, non-conforming, and not adoptable as a project "
            "palette. They carry no high-contrast sibling of their own.",
            "",
            "## Choosing a theme",
            "",
            _slug_table_md(themes),
            "",
            "Open the Command Palette → **Preferences: Color Theme** and pick one by its Name column above.",
            "",
            "## Installation",
            "",
        ]
        if meta.ship_vsix:
            readme_lines += [
                "1. Open the Command Palette (`Ctrl+Shift+P`).",
                "2. Run **Extensions: Install from VSIX…**",
                f"3. Select `{meta.name}-2.0.0.vsix`.",
                "4. Open the Command Palette → **Preferences: Color Theme** → "
                f"select **{default_theme.name}** (or any theme from the table "
                "above).",
            ]
        else:
            readme_lines += [
                "1. Copy this folder into the editor's extensions directory.",
                "2. Restart the editor.",
                "3. Open the Command Palette → **Preferences: Color Theme** → "
                f"select **{default_theme.name}** (or any theme from the table "
                "above).",
            ]
        readme_lines += [
            "",
            f"## {default_theme.name} — the default palette",
            "",
            _role_table_md(default_theme),
            "",
            "## License",
            "",
            "Copyright (C) 2026 Mohamed Hammad. Distributed under the GNU General Public License v3.0-or-later.",
            "",
            "---",
            "*Part of the Spacecraft Software Ecosystem.*",
            "",
        ]

        files = {
            "package.json": json.dumps(package, indent=2) + "\n",
            "README.md": "\n".join(readme_lines),
        }

        if meta.ship_vsix:
            manifest_lines = [
                '<?xml version="1.0" encoding="utf-8"?>',
                '<PackageManifest Version="2.0.0" '
                'xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" '
                'xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">',
                "  <Metadata>",
                f'    <Identity Language="en-US" Id="{meta.name}" Version="2.0.0" Publisher="Spacecraft-Software" />',
                f"    <DisplayName>{meta.display_name}</DisplayName>",
                f'    <Description xml:space="preserve">{meta.description}</Description>',
                "    <Tags>theme,color-theme,__web_extension</Tags>",
                "    <Categories>Themes</Categories>",
                "    <GalleryFlags>Public</GalleryFlags>",
                "    <Properties>",
                '      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.60.0" />',
                '      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui,workspace,web" />',
                '      <Property Id="Microsoft.VisualStudio.Services.Links.Source" '
                'Value="https://github.com/Spacecraft-Software/Theme.git" />',
                '      <Property Id="Microsoft.VisualStudio.Services.Links.GitHub" '
                'Value="https://github.com/Spacecraft-Software/Theme.git" />',
                '      <Property Id="Microsoft.VisualStudio.Services.Links.Support" '
                'Value="https://github.com/Spacecraft-Software/Theme/issues" />',
                '      <Property Id="Microsoft.VisualStudio.Services.GitHubFlavoredMarkdown" Value="true" />',
                '      <Property Id="Microsoft.VisualStudio.Services.Content.Pricing" Value="Free" />',
                "    </Properties>",
                "    <License>extension/LICENSE</License>",
                "  </Metadata>",
                "  <Installation>",
                '    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>',
                "  </Installation>",
                "  <Dependencies/>",
                "  <Assets>",
                '    <Asset Type="Microsoft.VisualStudio.Code.Manifest" '
                'Path="extension/package.json" Addressable="true" />',
                '    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" '
                'Path="extension/README.md" Addressable="true" />',
                '    <Asset Type="Microsoft.VisualStudio.Services.Content.License" '
                'Path="extension/LICENSE" Addressable="true" />',
                '    <Asset Type="Microsoft.VisualStudio.Services.Icons.Default" '
                'Path="extension/icon.png" Addressable="true" />',
                "  </Assets>",
                "</PackageManifest>",
            ]
            files["extension.vsixmanifest"] = "\n".join(manifest_lines) + "\n"
            content_types = (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Default Extension=".json" ContentType="application/json"/>'
                '<Default Extension=".md" ContentType="text/markdown"/>'
                '<Default Extension=".png" ContentType="image/png"/>'
                '<Default Extension=".vsixmanifest" ContentType="text/xml"/>'
                '<Override PartName="/extension/LICENSE" ContentType="text/plain"/>'
                "</Types>\n"
            )
            files["[Content_Types].xml"] = content_types

        return files

    return render_bundle


def _make_target(
    *,
    target_id: str,
    target_dir: str,
    meta: _PackageMeta,
    legacy_files: tuple[str, ...],
    archives: tuple[Archive, ...],
) -> Target:
    return Target(
        id=target_id,
        target_dir=target_dir,
        render=render,
        supports_mono=False,
        render_bundle=_make_render_bundle(meta),
        legacy_files=legacy_files,
        archives=archives,
        description=f"{meta.display_name} — themes/<slug>.json + package.json",
    )


_VSCODE_META = _PackageMeta(
    name="themes",
    display_name="Spacecraft Software Themes",
    description=(
        "The full Steelbore palette family (The Steelbore Standard §11) as a "
        "VS Code theme collection — Steelbore default, ten alternates, "
        "high-contrast siblings, and the Solarized fidelity pair."
    ),
    homepage="https://SpacecraftSoftware.org",
    ship_vsix=True,
)

_ANTIGRAVITY_META = _PackageMeta(
    name="themes-antigravity",
    display_name="Spacecraft Software Themes for Antigravity",
    description=(
        "The full Steelbore palette family (The Steelbore Standard §11) as a "
        "Google Antigravity theme collection — Steelbore default, ten "
        "alternates, high-contrast siblings, and the Solarized fidelity pair."
    ),
    homepage="https://github.com/Spacecraft-Software/Theme",
    ship_vsix=True,
)


def _vsix_archive(target_dir: str, name: str) -> Archive:
    return Archive(
        path=f"{target_dir}/{name}-2.0.0.vsix",
        fmt="vsix",
        entries=(
            ("extension.vsixmanifest", "extension.vsixmanifest"),
            ("[Content_Types].xml", "[Content_Types].xml"),
            ("package.json", "extension/package.json"),
            ("README.md", "extension/README.md"),
            ("LICENSE", "extension/LICENSE"),
            ("icon.png", "extension/icon.png"),
            ("themes", "extension/themes"),
        ),
    )


TARGETS = (
    _make_target(
        target_id="vscode",
        target_dir="Editors/VSCode/spacecraft-software-theme",
        meta=_VSCODE_META,
        legacy_files=(
            "themes/Spacecraft-Software-color-theme.json",
            "../settings.json",
            "spacecraft-software-1.0.0.vsix",
            "spacecraft-software-2.0.0.vsix",
        ),
        archives=(
            Archive(
                path="Editors/VSCode/spacecraft-software-vscode-theme.zip",
                fmt="zip",
                entries=(
                    ("themes", "themes"),
                    ("package.json", "package.json"),
                    ("README.md", "README.md"),
                    ("LICENSE", "LICENSE"),
                    ("../INSTALL.md", "INSTALL.md"),
                ),
            ),
            _vsix_archive("Editors/VSCode/spacecraft-software-theme", _VSCODE_META.name),
        ),
    ),
    _make_target(
        target_id="antigravity",
        target_dir="Editors/Google_Antigravity/spacecraft-software-antigravity",
        meta=_ANTIGRAVITY_META,
        legacy_files=("themes/Spacecraft-Software-color-theme.json",),
        archives=(
            Archive(
                path="Editors/Google_Antigravity/spacecraft-software-antigravity-theme.zip",
                fmt="zip",
                entries=(
                    ("themes", "themes"),
                    ("package.json", "package.json"),
                    ("README.md", "README.md"),
                    ("LICENSE", "LICENSE"),
                    ("../INSTALL.md", "INSTALL.md"),
                ),
            ),
            _vsix_archive(
                "Editors/Google_Antigravity/spacecraft-software-antigravity",
                _ANTIGRAVITY_META.name,
            ),
        ),
    ),
)
