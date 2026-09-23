# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""GNOME Terminal — dconf profile-installer renderer.

GNOME Terminal keeps no on-disk theme file of its own; a "theme" is a
profile registered in dconf under
``/org/gnome/terminal/legacy/profiles:/``.  So instead of a static config
file, each theme renders a POSIX ``sh`` installer script that creates its
own dconf profile (``visible-name``, colours, cursor, selection and the
16-slot ANSI palette) and appends the new profile's UUID to the profile
list, following the shape of the hand-written legacy script this replaces.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme

_PROFILE_PATH_VAR = "PROFILE_PATH"


def _dconf_string(key: str, hex_value: str) -> str:
    """A ``dconf write`` line for a GVariant string value (single-quoted)."""
    return f'dconf write "${{{_PROFILE_PATH_VAR}}}{key}" "\'{hex_value}\'"'


def _dconf_bool(key: str, value: bool) -> str:
    """A ``dconf write`` line for a GVariant boolean value (bare, unquoted)."""
    literal = "true" if value else "false"
    return f'dconf write "${{{_PROFILE_PATH_VAR}}}{key}" {literal}'


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.sh`` dconf-profile installer per theme."""
    header = theme.header("GNOME Terminal theme (dconf profile installer)").rstrip("\n")

    # Cursor and selection follow the kitty reference renderer: the cursor is
    # a foreground-filled block with background-coloured text under it, and
    # the selection fill is the accent role (role table: "selection fill" is
    # an accent use), with background text on top of it — the same verified
    # pair measured the other way round (§11 rule 3).
    palette_literal = "[" + ", ".join(f"'{c}'" for c in theme.ansi16()) + "]"

    lines = [
        "#!/bin/sh",
        header,
        "",
        f"# Creates the {theme.name!r} GNOME Terminal profile via dconf.",
        "#",
        "# Requires: dconf(1) and uuidgen(1). When uuidgen is missing, a",
        "# deterministic id is derived from a checksum instead (documented",
        "# below) so the script still runs.",
        "#",
        "# GNOME Terminal keys a profile by UUID, not by visible-name, so this",
        "# script is idempotent-ish rather than idempotent: re-running it never",
        "# edits a profile an earlier run created, it creates another one with",
        "# the same visible-name. When that happens it warns to stderr and",
        "# keeps going, matching the legacy installer's behaviour.",
        "#",
        "# GNOME Terminal's legacy profile schema has no light/dark flag of its",
        "# own; a light theme is expressed here purely through its background",
        "# and foreground colours, which is all VTE reads.",
        "",
        "set -eu",
        "",
        f"PROFILE_NAME='{theme.name}'",
        "PROFILES_ROOT=/org/gnome/terminal/legacy/profiles:/",
        "LIST_PATH=${PROFILES_ROOT}list",
        "",
        "if command -v uuidgen >/dev/null 2>&1; then",
        "    PROFILE_UUID=$(uuidgen)",
        "else",
        "    CHECKSUM=$(printf '%s' \"$PROFILE_NAME-$$-$(date +%s%N)\" | cksum | cut -d ' ' -f 1)",
        "    PROFILE_UUID=$(printf '00000000-0000-4000-8000-%012d' \"$CHECKSUM\")",
        "fi",
        "",
        'EXISTING=$(dconf read "$LIST_PATH" 2>/dev/null || true)',
        'EXISTING=$(printf "%s" "$EXISTING" | sed "s/^@as //")',
        'if [ -z "$EXISTING" ]; then',
        "    EXISTING='[]'",
        "fi",
        "",
        "# Warn (do not fail) if a profile with this visible-name is already",
        "# registered -- see the idempotency note above.",
        r"""for existing_uuid in $(printf "%s" "$EXISTING" | tr -d "[]" | tr "," "\n" | tr -d " '"); do""",
        '    [ -z "$existing_uuid" ] && continue',
        '    existing_name=$(dconf read "${PROFILES_ROOT}:$existing_uuid/visible-name" 2>/dev/null || true)',
        '    if [ "$existing_name" = "\'$PROFILE_NAME\'" ]; then',
        "        printf 'warning: a GNOME Terminal profile named \"%s\" already exists (uuid %s); '"
        '\'creating another one\\n\' "$PROFILE_NAME" "$existing_uuid" >&2',
        "    fi",
        "done",
        "",
        r"""NEW_LIST=$(printf "%s" "$EXISTING" | sed "s/]/, '$PROFILE_UUID']/" | sed "s/\[, /[/")""",
        'dconf write "$LIST_PATH" "$NEW_LIST"',
        "",
        f'{_PROFILE_PATH_VAR}="${{PROFILES_ROOT}}:$PROFILE_UUID/"',
        "",
        f'dconf write "${{{_PROFILE_PATH_VAR}}}visible-name" "\'$PROFILE_NAME\'"',
        _dconf_bool("use-theme-colors", False),
        _dconf_string("background-color", theme.background),
        _dconf_string("foreground-color", theme.foreground),
        _dconf_bool("bold-color-same-as-fg", False),
        _dconf_string("bold-color", theme.foreground),
        _dconf_bool("bold-is-bright", True),
        _dconf_bool("cursor-colors-set", True),
        _dconf_string("cursor-background-color", theme.foreground),
        _dconf_string("cursor-foreground-color", theme.background),
        _dconf_bool("highlight-colors-set", True),
        _dconf_string("highlight-background-color", theme.text_safe_accent),
        _dconf_string("highlight-foreground-color", theme.background),
        f'dconf write "${{{_PROFILE_PATH_VAR}}}palette" "{palette_literal}"',
        "",
        "printf '%s profile created for GNOME Terminal.\\n' \"$PROFILE_NAME\"",
        'printf \'Open GNOME Terminal -> Preferences -> Profiles -> select "%s".\\n\' "$PROFILE_NAME"',
        "",
    ]
    return {f"themes/{theme.slug}.sh": "\n".join(lines)}


TARGET = Target(
    id="gnome_terminal",
    target_dir="Terminals/GNOME_Terminal",
    render=render,
    supports_mono=False,
    legacy_files=("spacecraft-software-gnome-terminal.sh",),
    archives=(
        Archive(
            path="Terminals/spacecraft-software-gnome_terminal.zip",
            fmt="zip",
            entries=(("themes", "themes"), ("INSTALL.md", "INSTALL.md")),
        ),
    ),
    description="GNOME Terminal dconf profile installers (themes/<slug>.sh)",
)
