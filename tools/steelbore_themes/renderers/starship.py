# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Starship prompt — Catppuccin Powerline preset adaptation.

Upstream-preset adaptation (tools/AGENTS.md's ``Shells/Starship/starship.toml``
pattern): the legacy hand-written file ports the official
``catppuccin-powerline`` preset (https://starship.rs/presets/catppuccin-powerline)
verbatim -- format string and every ``[module]`` table untouched -- and only
renames ``[palettes.catppuccin_mocha]`` to ``[palettes.spacecraft_software]``.
This renderer keeps that pattern: :data:`_PRESET_BODY` is the preset's format
string and module tables, copied unchanged (the ``palette = 'spacecraft_software'``
line and the ``[palettes.spacecraft_software]`` table *name* are part of it and
stay fixed so the format string above never has to change), and only the
*values* inside the final ``[palettes.spacecraft_software]`` table are rebuilt
per theme from role tokens.

Mono (``steelbore-mono``): Starship (``nu-ansi-term``) has no bare ``default``
or ``reverse-video`` colour token. Steelbore Mono's own ``background`` /
``foreground`` / ``surface`` roles resolve to ``"default"`` and its ``focus``
role to ``"reverse-video"`` (tools/README.md rule 7) -- neither is a Starship
colour name, so :func:`_color` substitutes the canonical ANSI-slot name for
that role instead (tools/README.md rule 10: black=background, cyan=focus,
white=foreground). Every other mono role (``error`` -> ``red``, ``success`` ->
``green``, ``warning`` -> ``yellow``, ``structure`` -> ``blue``, ``accent`` ->
``bright-white``) is already a valid Starship name and passes through
unchanged.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from steelbore_themes.renderers import Target

if TYPE_CHECKING:
    from collections.abc import Mapping

    from steelbore_themes.core import Theme

# The upstream catppuccin-powerline preset, format string and every
# [module] table, verbatim -- only the trailing [palettes.*] table's values
# are theme-specific and are appended by render(). Do not hand-edit this
# body; port changes from the upstream preset the same way the legacy file
# did.
_PRESET_BODY: Final[str] = r'''"$schema" = 'https://starship.rs/config-schema.json'

format = """
[](red)\
$os\
$username\
[](bg:peach fg:red)\
$directory\
[](bg:yellow fg:peach)\
$git_branch\
$git_status\
[](fg:yellow bg:green)\
$c\
$rust\
$golang\
$nodejs\
$bun\
$php\
$java\
$kotlin\
$haskell\
$python\
[](fg:green bg:sapphire)\
$conda\
[](fg:sapphire bg:lavender)\
$time\
[ ](fg:lavender)\
$cmd_duration\
$line_break\
$character"""

palette = 'spacecraft_software'

[os]
disabled = false
style = "bg:red fg:crust"

[os.symbols]
Windows = ""
Ubuntu = "󰕈"
SUSE = ""
Raspbian = "󰐿"
Mint = "󰣭"
Macos = "󰀵"
Manjaro = ""
Linux = "󰌽"
Gentoo = "󰣨"
Fedora = "󰣛"
Alpine = ""
Amazon = ""
Android = ""
AOSC = ""
Arch = "󰣇"
Artix = "󰣇"
CentOS = ""
Debian = "󰣚"
Redhat = "󱄛"
RedHatEnterprise = "󱄛"

[username]
show_always = true
style_user = "bg:red fg:crust"
style_root = "bg:red fg:crust"
format = '[ $user]($style)'

[directory]
style = "bg:peach fg:crust"
format = "[ $path ]($style)"
truncation_length = 3
truncation_symbol = "…/"

[directory.substitutions]
"Documents" = "󰈙 "
"Downloads" = " "
"Music" = "󰝚 "
"Pictures" = " "
"Developer" = "󰲋 "

[git_branch]
symbol = ""
style = "bg:yellow"
format = '[[ $symbol $branch ](fg:crust bg:yellow)]($style)'

[git_status]
style = "bg:yellow"
format = '[[($all_status$ahead_behind )](fg:crust bg:yellow)]($style)'

[nodejs]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[bun]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[c]
symbol = " "
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[rust]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[golang]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[php]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[java]
symbol = " "
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[kotlin]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[haskell]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version) ](fg:crust bg:green)]($style)'

[python]
symbol = ""
style = "bg:green"
format = '[[ $symbol( $version)(\(#$virtualenv\)) ](fg:crust bg:green)]($style)'

[docker_context]
symbol = ""
style = "bg:sapphire"
format = '[[ $symbol( $context) ](fg:crust bg:sapphire)]($style)'

[conda]
symbol = "  "
style = "fg:crust bg:sapphire"
format = '[$symbol$environment ]($style)'
ignore_base = false

[time]
disabled = false
time_format = "%R"
style = "bg:lavender"
format = '[[  $time ](fg:crust bg:lavender)]($style)'

[line_break]
disabled = true

[character]
disabled = false
success_symbol = '[❯](bold fg:green)'
error_symbol = '[❯](bold fg:red)'
vimcmd_symbol = '[❮](bold fg:green)'
vimcmd_replace_one_symbol = '[❮](bold fg:lavender)'
vimcmd_replace_symbol = '[❮](bold fg:lavender)'
vimcmd_visual_symbol = '[❮](bold fg:yellow)'

[cmd_duration]
show_milliseconds = true
format = " in $duration "
style = "bg:lavender"
disabled = false
show_notifications = true
min_time_to_notify = 45000'''


def _color(value: str, *, mono_fallback: str) -> str:
    """``value`` (a role's resolved hex, or Steelbore Mono's ANSI role name)
    as a Starship-safe colour token.

    Hex themes: ``value`` is already a ``#RRGGBB`` Starship accepts verbatim.
    Steelbore Mono: ``"default"`` and ``"reverse-video"`` have no Starship
    equivalent, so they fall back to ``mono_fallback`` (the canonical
    ANSI-slot name for that role, tools/README.md rule 10); every other mono
    role name (``"red"``, ``"green"``, ``"yellow"``, ``"blue"``,
    ``"bright-white"``, ...) is already valid and passes through.
    """
    if value in ("default", "reverse-video"):
        return mono_fallback
    return value


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.toml`` per theme."""
    header = theme.header("Starship prompt theme (catppuccin-powerline preset, Spacecraft Software palette)").rstrip(
        "\n"
    )

    c_bg = _color(theme.background, mono_fallback="black")
    c_surface = _color(theme.surface, mono_fallback="black")
    c_structure = _color(theme.structure, mono_fallback="blue")
    c_success = _color(theme.success, mono_fallback="green")
    c_focus = _color(theme.focus, mono_fallback="cyan")
    c_error = _color(theme.error, mono_fallback="red")
    c_accent = _color(theme.accent, mono_fallback="bright-white")
    c_fg = _color(theme.foreground, mono_fallback="white")

    palette_lines = [
        "# ------------------------------------------------------------------------------",
        "# PALETTE DEFINITION — Spacecraft Software",
        "# Catppuccin role keys are preserved (red, peach, yellow, green, sapphire,",
        "# lavender, crust, …) so the upstream preset layout above renders unchanged,",
        "# but every value resolves to a role token from this theme",
        "# (Steelbore Standard §11.1) instead of a Catppuccin hue.",
        "# ------------------------------------------------------------------------------",
        "[palettes.spacecraft_software]",
        "# Powerline section accents (used as block backgrounds in the format string,",
        "# with crust text rendered directly on top). This is a fill + inverted",
        "# background-role text pairing, not accent-as-foreground-text, so peach uses",
        "# plain accent -- text_safe_accent's restriction doesn't apply here (tools/",
        "# README.md rule 3): the same contrast ratio measured the other way is a",
        "# verified pairing regardless of the accent's text-safety restriction.",
        f'red       = "{c_error}"      # error',
        f'peach     = "{c_accent}"      # accent',
        f'yellow    = "{c_structure}"      # structure',
        f'green     = "{c_success}"      # success',
        f'sapphire  = "{c_focus}"      # focus',
        f'lavender  = "{c_structure}"      # structure',
        "",
        "# Canvas — also the text colour on top of the bright section blocks above",
        f'crust     = "{c_bg}"',
        f'mantle    = "{c_bg}"',
        f'base      = "{c_bg}"',
        "",
        "# Secondary surfaces",
        f'surface0  = "{c_surface}"',
        f'surface1  = "{c_surface}"',
        f'surface2  = "{c_surface}"',
        "",
        "# Dim / muted scale",
        f'overlay0  = "{c_structure}"',
        f'overlay1  = "{c_structure}"',
        f'overlay2  = "{c_structure}"',
        "",
        "# Foreground text scale",
        f'text      = "{c_fg}"',
        f'subtext0  = "{c_fg}"',
        f'subtext1  = "{c_fg}"',
        "",
        "# Remaining catppuccin role keys mapped to the nearest Spacecraft Software role",
        f'rosewater = "{c_error}"',
        f'flamingo  = "{c_error}"',
        f'pink      = "{c_error}"',
        f'mauve     = "{c_error}"',
        f'maroon    = "{c_error}"',
        f'teal      = "{c_focus}"',
        f'sky       = "{c_focus}"',
        f'blue      = "{c_structure}"',
        "",
    ]

    content = header + "\n" + _PRESET_BODY + "\n\n" + "\n".join(palette_lines)
    return {f"themes/{theme.slug}.toml": content}


TARGET = Target(
    id="starship",
    target_dir="Shells/Starship",
    render=render,
    supports_mono=True,
    legacy_files=("starship.toml",),
    description="Starship prompt themes, catppuccin-powerline preset (themes/<slug>.toml)",
)
