# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Alacritty terminal — theme renderer.

Renders one theme per TOML file under themes/ (themes/<slug>.toml).
Alacritty >= 0.13 reads [colors.*] tables; light themes are flagged via
the [window] colors.alpha option and general.live_config_reload.
"""

from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING, TypeAlias

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme


TomlScalar: TypeAlias = "str | bool | int"
TomlTable: TypeAlias = "dict[str, TomlScalar | TomlTable]"


def _value_to_toml_str(value: TomlScalar) -> str:
    """Format a single value for TOML."""
    if isinstance(value, str) and value.startswith("#"):
        return f'"{value}"'
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _dict_to_toml(data: TomlTable) -> str:
    """Convert a dict to TOML format with proper nested section headers."""
    lines: list[str] = []

    def flatten_and_output(d: TomlTable, prefix: str = "") -> None:
        """Recursively flatten and output TOML sections."""
        sections: dict[str, TomlTable] = {}
        simple_values: dict[str, TomlScalar] = {}

        for key, value in d.items():
            if isinstance(value, dict):
                sections[key] = value
            else:
                simple_values[key] = value

        # Output simple key-values first (if any)
        for k, v in simple_values.items():
            lines.append(f"{k} = {_value_to_toml_str(v)}")

        # Then output each nested section
        for section_name, section_data in sections.items():
            section_path = f"{prefix}.{section_name}" if prefix else section_name
            lines.append(f"[{section_path}]")
            flatten_and_output(section_data, section_path)

    # Start with the root "colors" section
    colors = data.get("colors")
    if isinstance(colors, dict):
        lines.append("[colors]")
        flatten_and_output(colors, "colors")

    return "\n".join(lines)


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.toml`` per theme."""
    # Build the color configuration structure
    colors_config: TomlTable = {
        "primary": {
            "background": theme.background,
            "foreground": theme.foreground,
        },
        "cursor": {
            "text": theme.background,
            "cursor": theme.foreground,
        },
        "vi_mode_cursor": {
            "text": theme.background,
            "cursor": theme.accent,
        },
        "selection": {
            "text": theme.background,
            "background": theme.text_safe_accent,
        },
        "search": {
            "matches": {
                "foreground": theme.background,
                "background": theme.text_safe_accent,
            },
            "focused_match": {
                "foreground": theme.background,
                "background": theme.structure,
            },
        },
        "hints": {
            "foreground": theme.background,
            "background": theme.text_safe_accent,
            "border": theme.structure,
        },
        "line_indicator": {
            "foreground": theme.focus,
            "background": theme.surface_alt,
        },
        "footer_bar": {
            "background": theme.surface,
            "foreground": theme.foreground,
        },
        "normal": {
            "black": theme.ansi["black"],
            "red": theme.ansi["red"],
            "green": theme.ansi["green"],
            "yellow": theme.ansi["yellow"],
            "blue": theme.ansi["blue"],
            "magenta": theme.ansi["magenta"],
            "cyan": theme.ansi["cyan"],
            "white": theme.ansi["white"],
        },
        "bright": {
            "black": theme.ansi_bright["black"],
            "red": theme.ansi_bright["red"],
            "green": theme.ansi_bright["green"],
            "yellow": theme.ansi_bright["yellow"],
            "blue": theme.ansi_bright["blue"],
            "magenta": theme.ansi_bright["magenta"],
            "cyan": theme.ansi_bright["cyan"],
            "white": theme.ansi_bright["white"],
        },
    }

    # Build the complete TOML structure
    toml_data: TomlTable = {"colors": colors_config}

    # Build content: header + TOML
    header = theme.header("Alacritty terminal theme").rstrip("\n")
    toml_text = _dict_to_toml(toml_data)

    content = f"{header}\n\n{toml_text}\n"

    # Validate TOML parses correctly (no temp file needed).
    try:
        tomllib.loads(content)
    except Exception as e:
        msg = f"TOML validation failed for {theme.slug}: {e}"
        raise ValueError(msg) from e

    return {f"themes/{theme.slug}.toml": content}


TARGET = Target(
    id="alacritty",
    target_dir="Terminals/Alacritty",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software.toml",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-alacritty.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="Alacritty terminal colour themes (include themes/<slug>.toml)",
)
