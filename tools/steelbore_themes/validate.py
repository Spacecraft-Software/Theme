# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Post-render validation.

Every generated file is checked for the things that can be checked without
knowing the format: text hygiene (§6.5), that every ``#RRGGBB`` it carries is a
colour the theme is allowed to emit (§11.4 — no tokens from another palette,
no lifted hex outside a high-contrast variant, none of the pre-generator
legacy colours), and that structured formats parse.
"""

from __future__ import annotations

import json
import re
import tomllib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from steelbore_themes.core import Theme

_HEX8_RE = re.compile(r"#([0-9A-Fa-f]{8})\b")
_HEX6_RE = re.compile(r"#([0-9A-Fa-f]{6})\b")

LEGACY_HEXES: frozenset[str] = frozenset(
    {
        # Pre-family colours invented in this repository; none belongs to a palette.
        "#050530",
        "#6272A4",
        "#E6E6F0",
        "#BD93F9",
        "#FE6B00",
        "#0E141D",
        "#142E46",
        "#F0F0F0",
        "#FF6E6E",
        "#69FF94",
        "#FFFFA5",
        "#D6ACFF",
        "#FF92DF",
        "#A4FFFF",
        "#10B981",
        "#3B82F6",
        "#4B5563",
        "#2ECC71",
    }
)


@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def _hexes(content: str) -> tuple[set[str], set[tuple[str, str]]]:
    """``(six_digit, eight_digit)`` — six-digit hexes upper-cased with ``#``,
    and eight-digit tokens as ``(#prefix6, #suffix6)`` pairs so both the
    ``#RRGGBBAA`` (CSS, Zed) and ``#AARRGGBB`` (Visual Studio) conventions can
    be judged: a token passes when either window is a palette colour."""
    eight = {(f"#{m.group(1)[:6].upper()}", f"#{m.group(1)[2:].upper()}") for m in _HEX8_RE.finditer(content)}
    # Strip 8-digit tokens first so their windows are not double-counted.
    stripped = _HEX8_RE.sub("", content)
    six = {f"#{m.group(1).upper()}" for m in _HEX6_RE.finditer(stripped)}
    return six, eight


def _judge(
    path: str, six: set[str], eight: set[tuple[str, str]], allowed: frozenset[str], scope: str
) -> Iterable[Finding]:
    for hex_value in sorted(six):
        if hex_value in LEGACY_HEXES:
            yield Finding(path, f"legacy pre-family colour {hex_value} (§11.4)")
        elif hex_value not in allowed:
            yield Finding(path, f"{hex_value} is not a {scope} colour (§11.4)")
    for prefix, suffix in sorted(eight):
        if prefix in LEGACY_HEXES or suffix in LEGACY_HEXES:
            yield Finding(path, f"legacy pre-family colour in {prefix}/{suffix} (§11.4)")
        elif prefix not in allowed and suffix not in allowed:
            yield Finding(path, f"8-digit {prefix}.. is not a {scope} colour (§11.4)")


def _check_text(path: str, content: str) -> Iterable[Finding]:
    if "\r" in content:
        yield Finding(path, "carriage return present (§6.5 requires LF)")
    if content.startswith("﻿"):
        yield Finding(path, "byte-order mark present (§6.5)")
    if content and not content.endswith("\n"):
        yield Finding(path, "missing final newline (§6.5)")
    if "\t" in content and path.endswith((".json", ".toml", ".yaml", ".yml")):
        # Not an error, but tabs in data files are unusual enough to flag.
        pass


def _check_parse(path: str, content: str) -> Iterable[Finding]:
    lower = path.lower()
    try:
        if lower.endswith(".json"):
            json.loads(content)
        elif lower.endswith(".toml"):
            tomllib.loads(content)
        elif lower.endswith((".xml", ".plist", ".itermcolors", ".vstheme", ".vsixmanifest")):
            ET.fromstring(content.encode("utf-8"))
    except (ValueError, ET.ParseError) as exc:
        yield Finding(path, f"does not parse: {exc}")


def check_theme_files(theme: Theme, files: Mapping[str, str]) -> list[Finding]:
    """Validate one theme's rendered files."""
    findings: list[Finding] = []
    allowed = theme.allowed_hexes()
    for path, content in files.items():
        findings.extend(_check_text(path, content))
        findings.extend(_check_parse(path, content))
        six, eight = _hexes(content)
        if theme.is_mono and (six or eight):
            findings.append(Finding(path, "mono theme must not carry hex colours"))
            continue
        findings.extend(_judge(path, six, eight, allowed, theme.palette_slug))
    return findings


def check_bundle_files(files: Mapping[str, str], allowed: frozenset[str]) -> list[Finding]:
    """Validate package-level files, which may reference any family theme."""
    findings: list[Finding] = []
    for path, content in files.items():
        findings.extend(_check_text(path, content))
        findings.extend(_check_parse(path, content))
        six, eight = _hexes(content)
        findings.extend(_judge(path, six, eight, allowed, "family"))
    return findings
