# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""JetBrains IDE themes (IntelliJ Platform) — one plugin per vendor directory.

One format — a ``*.theme.json`` UI theme plus a ``*.xml`` editor colour scheme
— serves two Spacecraft Software targets that differ only in plugin id,
plugin name, and directory: ``jetbrains`` (IntelliJ IDEA, RustRover, GoLand,
PyCharm, WebStorm, CLion, Rider, …) and ``android_studio``. Each theme also
gets a standalone ``.icls`` copy of its editor scheme for
Settings > Editor > Color Scheme > Import, and the bundle file
(``src/META-INF/plugin.xml``) lists one ``<themeProvider>`` per registered
hex theme.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.core import (
    ANSI_SLOTS,
    CONTACT,
    COPYRIGHT_YEAR,
    MAINTAINER,
    PROJECT_URL,
    Theme,
)
from steelbore_themes.renderers import Archive, BundleFn, Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

_ANSI_NAMES: dict[str, str] = {
    "black": "BLACK",
    "red": "RED",
    "green": "GREEN",
    "yellow": "YELLOW",
    "blue": "BLUE",
    "magenta": "MAGENTA",
    "cyan": "CYAN",
    "white": "WHITE",
}


def _attr(name: str, **opts: str) -> list[str]:
    """One ``<option name="NAME"><value>...</value></option>`` block."""
    lines = [f'    <option name="{name}">', "      <value>"]
    lines += [f'        <option name="{k}" value="{v}" />' for k, v in opts.items()]
    lines += ["      </value>", "    </option>"]
    return lines


def _scheme_xml(theme: Theme, ide: str) -> str:
    """The editor colour scheme, shared verbatim by ``src/<slug>.xml`` and
    ``themes/<slug>.icls``."""
    parent = "Darcula" if theme.is_dark else "Default"
    fg, bg = theme.hex_bare("foreground"), theme.hex_bare("background")
    accent, structure = theme.hex_bare("accent"), theme.hex_bare("structure")
    accent_safe = theme.text_safe_accent.lstrip("#")
    success, error = theme.hex_bare("success"), theme.hex_bare("error")
    warning, focus = theme.hex_bare("warning"), theme.hex_bare("focus")

    lines = [f'<scheme name="{theme.name}" version="142" parent_scheme="{parent}">']
    lines.append(theme.header_block("JetBrains editor colour scheme", "<!--", "-->").rstrip("\n"))
    lines += [
        "  <metaInfo>",
        '    <property name="created">2026-09-23T00:00:00</property>',
        f'    <property name="ide">{ide}</property>',
        "  </metaInfo>",
        "  <colors>",
        f'    <option name="CARET_ROW_COLOR" value="{theme.hex_bare("surface")}" />',
        f'    <option name="CONSOLE_BACKGROUND_KEY" value="{theme.hex_bare("surface-alt")}" />',
        f'    <option name="GUTTER_BACKGROUND" value="{bg}" />',
        f'    <option name="INDENT_GUIDE" value="{structure}" />',
        f'    <option name="LINE_NUMBERS_COLOR" value="{structure}" />',
        f'    <option name="SELECTION_BACKGROUND" value="{accent}" />',
        f'    <option name="SELECTION_FOREGROUND" value="{bg}" />',
        f'    <option name="WHITESPACES" value="{structure}" />',
        f'    <option name="RIGHT_MARGIN_COLOR" value="{structure}" />',
        f'    <option name="TEARLINE_COLOR" value="{structure}" />',
        f'    <option name="SOFT_WRAP_SIGN_COLOR" value="{structure}" />',
        "  </colors>",
        "  <attributes>",
    ]
    lines += _attr("TEXT", FOREGROUND=fg, BACKGROUND=bg)
    lines += _attr("DEFAULT_KEYWORD", FOREGROUND=accent_safe, FONT_TYPE="1")
    lines += _attr("DEFAULT_STRING", FOREGROUND=success)
    lines += _attr("DEFAULT_NUMBER", FOREGROUND=warning)
    lines += _attr("DEFAULT_CONSTANT", FOREGROUND=warning)
    lines += _attr("DEFAULT_VALID_STRING_ESCAPE", FOREGROUND=accent_safe)
    lines += _attr("DEFAULT_FUNCTION_DECLARATION", FOREGROUND=focus)
    lines += _attr("DEFAULT_FUNCTION_CALL", FOREGROUND=focus)
    lines += _attr("DEFAULT_CLASS_NAME", FOREGROUND=structure)
    lines += _attr("DEFAULT_INTERFACE_NAME", FOREGROUND=structure)
    lines += _attr("DEFAULT_IDENTIFIER", FOREGROUND=fg)
    lines += _attr("DEFAULT_LOCAL_VARIABLE", FOREGROUND=fg)
    lines += _attr("DEFAULT_PARAMETER", FOREGROUND=fg)
    lines += _attr("DEFAULT_LINE_COMMENT", FOREGROUND=structure, FONT_TYPE="2")
    lines += _attr("DEFAULT_BLOCK_COMMENT", FOREGROUND=structure, FONT_TYPE="2")
    lines += _attr("DEFAULT_DOC_COMMENT", FOREGROUND=structure, FONT_TYPE="2")
    lines += _attr("DEFAULT_TAG", FOREGROUND=error)
    lines += _attr("DEFAULT_ATTRIBUTE", FOREGROUND=success)
    lines += _attr("BAD_CHARACTER", EFFECT_COLOR=error, EFFECT_TYPE="2")
    lines += _attr("ERRORS_ATTRIBUTES", EFFECT_COLOR=error, EFFECT_TYPE="2")
    lines += _attr("WARNING_ATTRIBUTES", EFFECT_COLOR=warning, EFFECT_TYPE="2")
    lines += _attr("TODO_DEFAULT_ATTRIBUTES", FOREGROUND=warning, FONT_TYPE="1")
    # Rust support (RustRover) — legacy src/spacecraft-software.xml carried
    # these; keep per-language keyword/macro/struct highlighting instead of
    # falling back to the parent scheme's generic defaults.
    lines += _attr("RUST_KEYWORD", FOREGROUND=accent_safe, FONT_TYPE="1")
    lines += _attr("RUST_MACRO", FOREGROUND=focus)
    lines += _attr("RUST_STRUCT", FOREGROUND=structure)
    # Go support (GoLand) — same rationale as the Rust block above.
    lines += _attr("GO_KEYWORD", FOREGROUND=accent_safe, FONT_TYPE="1")
    lines += _attr("GO_BUILTIN_FUNCTION", FOREGROUND=focus)
    lines += _attr("GO_STRUCT_EXPORTED", FOREGROUND=structure)
    for slot in ANSI_SLOTS:
        lines += _attr(f"CONSOLE_{_ANSI_NAMES[slot]}_OUTPUT", FOREGROUND=theme.ansi[slot].lstrip("#"))
    for slot in ANSI_SLOTS:
        lines += _attr(
            f"CONSOLE_{_ANSI_NAMES[slot]}_BRIGHT_OUTPUT",
            FOREGROUND=theme.ansi_bright[slot].lstrip("#"),
        )
    lines += ["  </attributes>", "</scheme>", ""]
    return "\n".join(lines)


def _theme_json(theme: Theme) -> str:
    """The IntelliJ Platform UI theme — ``colors`` (semantic component keys)
    plus ``ui`` (the common cross-IDE key families)."""
    colors: dict[str, str] = {
        "DefaultTabs.background": theme.surface,
        "DefaultTabs.underlineColor": theme.accent,
        "DefaultTabs.inactiveUnderlineColor": theme.border,
        "Editor.background": theme.background,
        "Editor.foreground": theme.foreground,
        "EditorTabs.background": theme.surface,
        "EditorTabs.underlineColor": theme.accent,
        "EditorTabs.inactiveUnderlineColor": theme.border,
        "EditorTabs.underlinedTabForeground": theme.foreground,
        "ToolWindow.Header.background": theme.surface,
        "ToolWindow.Header.inactiveBackground": theme.background,
        "ToolWindow.HeaderTab.selectedBackground": theme.accent,
        "ToolWindow.HeaderTab.selectedInactiveBackground": theme.surface,
        "SidePanel.background": theme.surface,
        "NavBar.background": theme.background,
        "StatusBar.background": theme.surface,
        "StatusBar.borderColor": theme.border,
        "StatusBar.foreground": theme.foreground,
    }
    ui: dict[str, str] = {
        "*.background": theme.background,
        "*.foreground": theme.foreground,
        "*.selectionBackground": theme.accent,
        "*.selectionForeground": theme.background,
        "Component.focusColor": theme.focus,
        "Button.startBackground": theme.surface,
        "Button.endBackground": theme.surface,
        "Button.foreground": theme.foreground,
        "Button.focusedBorderColor": theme.focus,
        "Button.default.startBackground": theme.accent,
        "Button.default.endBackground": theme.accent,
        "Button.default.foreground": theme.background,
        "Link.activeForeground": theme.structure,
        "Link.hoverForeground": theme.structure,
        "Link.visitedForeground": theme.structure,
        "Link.pressedForeground": theme.structure,
        "CheckBox.background": theme.background,
        "ComboBox.background": theme.background,
        "ComboBox.selectionBackground": theme.surface,
        "ComboBox.selectionForeground": theme.foreground,
        "Label.foreground": theme.foreground,
        "Label.infoForeground": theme.structure,
        "Label.errorForeground": theme.error,
        "Menu.background": theme.background,
        "Menu.selectionBackground": theme.surface,
        "Menu.selectionForeground": theme.foreground,
        "MenuItem.background": theme.background,
        "MenuItem.selectionBackground": theme.surface,
        "MenuItem.selectionForeground": theme.text_safe_accent,
        "Panel.background": theme.background,
        "Panel.foreground": theme.foreground,
        "ToolWindow.background": theme.background,
        "Tree.background": theme.surface,
        "Tree.foreground": theme.foreground,
        "Tree.selectionBackground": theme.accent,
        "Tree.selectionForeground": theme.background,
        "List.background": theme.surface,
        "List.foreground": theme.foreground,
        "List.selectionBackground": theme.accent,
        "List.selectionForeground": theme.background,
        "Table.background": theme.surface,
        "Table.foreground": theme.foreground,
        "Table.selectionBackground": theme.accent,
        "Table.selectionForeground": theme.background,
        "Table.gridColor": theme.border,
        "Popup.background": theme.surface,
        "Popup.borderColor": theme.border,
        "Notification.background": theme.surface,
        "Notification.foreground": theme.foreground,
        "Notification.borderColor": theme.border,
        "ProgressBar.progressColor": theme.accent,
        "ProgressBar.trackColor": theme.surface,
        "ProgressBar.failedColor": theme.error,
        "ProgressBar.passedColor": theme.success,
        "SearchMatch.startBackground": theme.with_alpha("accent", "40"),
        "SearchMatch.endBackground": theme.with_alpha("accent", "40"),
        "ValidationTooltip.errorBackground": theme.error,
        "ValidationTooltip.errorBorderColor": theme.error,
        "ValidationTooltip.warningBackground": theme.warning,
        "ValidationTooltip.warningBorderColor": theme.warning,
        "CompletionPopup.background": theme.surface,
        "CompletionPopup.foreground": theme.foreground,
        "CompletionPopup.selectionBackground": theme.accent,
        "CompletionPopup.selectionForeground": theme.background,
        "CompletionPopup.matchForeground": theme.text_safe_accent,
    }
    payload = {
        "name": theme.name,
        "author": "Mohamed Hammad",
        "dark": theme.is_dark,
        "editorScheme": f"/{theme.slug}.xml",
        "colors": colors,
        "ui": ui,
    }
    return json.dumps(payload, indent=2) + "\n"


def _render(theme: Theme, ide: str) -> Mapping[str, str]:
    scheme = _scheme_xml(theme, ide)
    return {
        f"src/{theme.slug}.theme.json": _theme_json(theme),
        f"src/{theme.slug}.xml": scheme,
        f"themes/{theme.slug}.icls": scheme,
    }


def _bundle_header() -> str:
    """A provenance header for ``plugin.xml``, which lists every hex theme and
    so is not any single :class:`Theme`'s own ``header_block``."""
    lines = [
        f"SPDX-FileCopyrightText: {COPYRIGHT_YEAR} {MAINTAINER} <{CONTACT}>",
        # REUSE-IgnoreStart
        "SPDX-License-Identifier: GPL-3.0-or-later",
        # REUSE-IgnoreEnd
        "",
        "GENERATED by tools/steelbore_themes from Steelbore/steelbore.toml. Do not edit by hand — regenerate.",
        "One <themeProvider> per registered hex theme (§11.6.1).",
        f"Maintainer: {MAINTAINER} <{CONTACT}> · {PROJECT_URL}",
    ]
    body = "\n".join(f" * {line}".rstrip() for line in lines)
    return f"<!--\n{body}\n -->"


def _make_render_bundle(plugin_id: str, plugin_name: str, description: tuple[str, ...]) -> BundleFn:
    def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
        lines = ["<idea-plugin>", _bundle_header()]
        lines += [
            f"  <id>{plugin_id}</id>",
            f"  <name>{plugin_name}</name>",
            "  <version>2.0</version>",
            '  <vendor email="support@SpacecraftSoftware.org" '
            'url="https://SpacecraftSoftware.org">Mohamed Hammad</vendor>',
            "",
            "  <description><![CDATA[",
        ]
        lines += [f"    {line}" for line in description]
        lines += [
            "  ]]></description>",
            "",
            "  <depends>com.intellij.modules.platform</depends>",
            "",
            '  <extensions defaultExtensionNs="com.intellij">',
        ]
        lines += [
            f'    <themeProvider id="{plugin_id}.{theme.slug}" path="/{theme.slug}.theme.json"/>' for theme in themes
        ]
        lines += ["  </extensions>", "</idea-plugin>", ""]
        return {"src/META-INF/plugin.xml": "\n".join(lines)}

    return render_bundle


_JETBRAINS_DESCRIPTION: tuple[str, ...] = (
    "The Spacecraft Software Steelbore palette family for JetBrains IDEs",
    "(IntelliJ IDEA, RustRover, GoLand, PyCharm, WebStorm, CLion, Rider, and",
    "every other JetBrains IDE).<br>",
    "Ships every registered hex theme — Steelbore and its alternates, each",
    "with a high-contrast sibling — as a selectable IDE theme plus a matching",
    "editor colour scheme.",
)

_ANDROID_STUDIO_DESCRIPTION: tuple[str, ...] = (
    "The Spacecraft Software Steelbore palette family for Android Studio.<br>",
    "Ships every registered hex theme — Steelbore and its alternates, each",
    "with a high-contrast sibling — as a selectable IDE theme plus a matching",
    "editor colour scheme.",
)

TARGETS = (
    Target(
        id="jetbrains",
        target_dir="Editors/JetBrains",
        render=lambda theme: _render(theme, "idea"),
        render_bundle=_make_render_bundle(
            "com.spacecraft-software.theme",
            "Spacecraft Software Theme",
            _JETBRAINS_DESCRIPTION,
        ),
        supports_mono=False,
        legacy_files=(
            "src/spacecraft-software.theme.json",
            "src/spacecraft-software.xml",
            "Spacecraft-Software.icls",
        ),
        archives=(
            Archive(
                path="Editors/JetBrains/spacecraft-software-jetbrains-theme.zip",
                fmt="zip",
                entries=(
                    ("src", "src"),
                    ("themes", "themes"),
                    ("INSTALL.md", "INSTALL.md"),
                    ("README.md", "README.md"),
                ),
            ),
        ),
        description="JetBrains IDE theme plugin (theme.json + editor scheme XML per theme)",
    ),
    Target(
        id="android_studio",
        target_dir="Editors/Android_Studio",
        render=lambda theme: _render(theme, "AndroidStudio"),
        render_bundle=_make_render_bundle(
            "com.spacecraft-software.android.theme",
            "Spacecraft Software Theme for Android Studio",
            _ANDROID_STUDIO_DESCRIPTION,
        ),
        supports_mono=False,
        legacy_files=(
            "src/spacecraft-software-android.theme.json",
            "src/spacecraft-software-android.xml",
        ),
        archives=(
            Archive(
                path="Editors/Android_Studio/spacecraft-software-androidstudio-theme.zip",
                fmt="zip",
                entries=(
                    ("src", "src"),
                    ("themes", "themes"),
                    ("INSTALL.md", "INSTALL.md"),
                    ("README.md", "README.md"),
                ),
            ),
        ),
        description="Android Studio theme plugin (theme.json + editor scheme XML per theme)",
    ),
)
