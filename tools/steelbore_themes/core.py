# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Palette-family model for the Spacecraft Software theme generator.

Loads ``Steelbore/steelbore.toml`` (the canonical §11 contract, copied verbatim
from the ``steelbore-color-palette`` skill) and exposes every registered theme as
an immutable :class:`Theme`.  Renderers consume :class:`Theme` objects and never
see a hex literal of their own: every colour a generated file carries is read
from the TOML through a role token (§11.1) or a named palette colour.

Boundary validation is done by hand against ``tomllib`` output rather than with
Pydantic so the tool runs on a bare ``python3`` (3.11+) with zero dependencies;
that is a documented trade-off, not an oversight.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping

ROLES: Final[tuple[str, ...]] = (
    "background",
    "surface",
    "surface-alt",
    "foreground",
    "accent",
    "structure",
    "success",
    "error",
    "warning",
    "focus",
    "border",
)
"""The eleven §11.1 role tokens, in contract order."""

CLASSIC_ROLES: Final[tuple[str, ...]] = (
    "background",
    "foreground",
    "accent",
    "success",
    "error",
    "info",
)
"""The legacy six-role contract bound by ``steelbore-classic`` (§11.2)."""

ANSI_SLOTS: Final[tuple[str, ...]] = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
)
"""ANSI colours 0-7 in index order; 8-15 are the ``bright_*`` siblings."""

ThemeKind = Literal["base", "high-contrast", "mono"]
Conformance = Literal["conforming", "legacy", "fidelity", "mono"]
Polarity = Literal["dark", "light"]

_HEX_RE: Final[re.Pattern[str]] = re.compile(r"^#[0-9A-Fa-f]{6}$")

MAINTAINER: Final[str] = "Mohamed Hammad"
CONTACT: Final[str] = "Mohamed.Hammad@SpacecraftSoftware.org"
PROJECT_URL: Final[str] = "https://Theme.SpacecraftSoftware.org/"
COPYRIGHT_YEAR: Final[str] = "2026"

DISPLAY_NAMES: Final[Mapping[str, str]] = {
    "steelbore": "Steelbore",
    "steelbore-classic": "Steelbore Classic",
    "steelbore-blue": "Steelbore Blue",
    "steelbore-magnetar": "Steelbore Magnetar",
    "steelbore-biolume": "Steelbore Biolume",
    "steelbore-navywhite": "Steelbore NavyWhite",
    "tokyonight": "Tokyo Night",
    "steelbore-hanzosteel": "Steelbore Hanzo Steel",
    "steelbore-blackpinkpanther": "Steelbore BlackPinkPanther",
    "steelbore-green": "Steelbore Green",
    "steelbore-greenalt": "Steelbore Green Alt",
    "solarized-dark": "Solarized Dark",
    "solarized-light": "Solarized Light",
    "steelbore-mono": "Steelbore Mono",
}

_HC_SUFFIX: Final[str] = "-high-contrast"


class PaletteError(ValueError):
    """The TOML did not have the shape the §11 contract promises."""


@dataclass(frozen=True, slots=True)
class Theme:
    """One registered theme: a palette plus a variant, fully resolved.

    ``roles`` maps every §11.1 role token to a ``#RRGGBB`` hex, except for the
    mono variant where the values are 4-bit ANSI names (``"red"``,
    ``"bright-white"``, ``"default"``, ``"reverse-video"``).  Classic binds the
    six-role contract; the missing five roles are filled with the documented
    fallbacks in :func:`_classic_roles` so renderers can treat every theme
    uniformly.
    """

    slug: str
    name: str
    palette_slug: str
    palette_name: str
    kind: ThemeKind
    polarity: Polarity
    conformance: Conformance
    roles: Mapping[str, str]
    palette: Mapping[str, str]
    restricted_roles: frozenset[str]
    contrast_vs_background: Mapping[str, str]
    non_role_fills: tuple[str, ...]
    family_version: str
    standard_version: str

    # -- role accessors -----------------------------------------------------

    @property
    def background(self) -> str:
        return self.roles["background"]

    @property
    def surface(self) -> str:
        return self.roles["surface"]

    @property
    def surface_alt(self) -> str:
        return self.roles["surface-alt"]

    @property
    def foreground(self) -> str:
        return self.roles["foreground"]

    @property
    def accent(self) -> str:
        return self.roles["accent"]

    @property
    def structure(self) -> str:
        return self.roles["structure"]

    @property
    def success(self) -> str:
        return self.roles["success"]

    @property
    def error(self) -> str:
        return self.roles["error"]

    @property
    def warning(self) -> str:
        return self.roles["warning"]

    @property
    def focus(self) -> str:
        return self.roles["focus"]

    @property
    def border(self) -> str:
        return self.roles["border"]

    @property
    def info(self) -> str:
        """Classic's ``info`` token; ``structure`` for every eleven-role palette."""
        return self.roles.get("info", self.roles["structure"])

    # -- classification -------------------------------------------------------

    @property
    def is_mono(self) -> bool:
        return self.kind == "mono"

    @property
    def is_high_contrast(self) -> bool:
        return self.kind == "high-contrast"

    @property
    def is_dark(self) -> bool:
        return self.polarity == "dark"

    @property
    def is_light(self) -> bool:
        return self.polarity == "light"

    @property
    def is_classic(self) -> bool:
        return self.palette_slug == "steelbore-classic"

    @property
    def is_fidelity(self) -> bool:
        return self.conformance == "fidelity"

    @property
    def text_safe_accent(self) -> str:
        """``accent`` where it clears 4.5:1, else ``structure``.

        Steelbore Blue's Electric Blue anchor is restricted to large text and
        non-text UI on every background (3.91:1).  A renderer that must put the
        accent role into a *normal-size text* slot uses this instead.
        """
        return self.structure if "accent" in self.restricted_roles else self.accent

    # -- ANSI -----------------------------------------------------------------

    @property
    def ansi(self) -> Mapping[str, str]:
        """ANSI 0-7 as ``slot -> hex`` (or ``slot -> ansi name`` for mono).

        Derivation (documented in ``AGENTS.md``): black=background,
        red=error, green=success, yellow=warning, blue=structure,
        magenta=accent (structure when the accent is text-restricted),
        cyan=focus, white=foreground.
        """
        if self.is_mono:
            return {slot: slot for slot in ANSI_SLOTS}
        return {
            "black": self.background,
            "red": self.error,
            "green": self.success,
            "yellow": self.warning,
            "blue": self.structure,
            "magenta": self.text_safe_accent,
            "cyan": self.focus,
            "white": self.foreground,
        }

    @property
    def ansi_bright(self) -> Mapping[str, str]:
        """ANSI 8-15.  Identical to 0-7 except bright-black, which becomes
        ``structure`` (a legible dim text colour; surface fills are never text,
        §11.0.1).  Lifted hexes are high-contrast-only (§11.1.1) and are
        deliberately *not* used as bright siblings of a base theme."""
        if self.is_mono:
            return {slot: f"bright-{slot}" for slot in ANSI_SLOTS}
        bright = dict(self.ansi)
        bright["black"] = self.structure
        return bright

    def ansi16(self) -> tuple[str, ...]:
        """ANSI 0-15 in index order."""
        return tuple(self.ansi[s] for s in ANSI_SLOTS) + tuple(self.ansi_bright[s] for s in ANSI_SLOTS)

    # -- colour conversions ---------------------------------------------------

    def rgb(self, role: str) -> tuple[int, int, int]:
        """``(r, g, b)`` integers for a role token.  Raises for mono themes."""
        return hex_to_rgb(self.roles[role])

    def rgb_float(self, role: str) -> tuple[float, float, float]:
        """``(r, g, b)`` floats in ``0.0-1.0`` (iTerm2 / COSMIC style)."""
        r, g, b = self.rgb(role)
        return (r / 255.0, g / 255.0, b / 255.0)

    def hex_bare(self, role: str) -> str:
        """``RRGGBB`` without the leading ``#`` (JetBrains XML, Ghostty)."""
        return self.roles[role].lstrip("#")

    def with_alpha(self, role: str, alpha_hex: str) -> str:
        """``#RRGGBBAA`` — a palette hex with a two-digit alpha suffix.

        Used only for translucent *fills* (selection, hover) over the canvas.
        The validator accepts an 8-digit hex when its 6-digit prefix is a
        palette colour.
        """
        if len(alpha_hex) != 2:
            msg = f"alpha must be two hex digits, got {alpha_hex!r}"
            raise ValueError(msg)
        return f"{self.roles[role]}{alpha_hex.upper()}"

    # -- allowed hexes for validation -----------------------------------------

    def allowed_hexes(self) -> frozenset[str]:
        """Every ``#RRGGBB`` this theme may emit, upper-cased.

        Role hexes plus the palette's named colours; lifted (``* Lift``)
        colours are permitted only in the high-contrast variant, and Classic's
        legacy names are permitted only inside Classic.
        """
        allowed: set[str] = set()
        for value in self.roles.values():
            if _HEX_RE.match(value):
                allowed.add(value.upper())
        for name, value in self.palette.items():
            if name.endswith(" Lift") and not self.is_high_contrast:
                continue
            allowed.add(value.upper())
        return frozenset(allowed)

    # -- headers --------------------------------------------------------------

    def header_lines(self, title: str) -> list[str]:
        """The provenance header every generated text file carries."""
        variant = {
            "base": "base",
            "high-contrast": "high-contrast (§11.1.1 accessible-mode sibling)",
            "mono": "mono (§11.1.1, 4-bit ANSI, NO_COLOR)",
        }[self.kind]
        conformance = {
            "conforming": "WCAG 2.2 AA verified against the palette canvas (§11)",
            "legacy": "legacy six-role contract (§11.2); measured against Void Navy",
            "fidelity": (
                "FIDELITY PALETTE (§11.5) — reproduced verbatim, NON-CONFORMING, not adoptable as a project palette"
            ),
            "mono": "palette-independent; defers hue to the terminal (§11.1.1)",
        }[self.conformance]
        # REUSE-IgnoreStart — these strings are emitted into generated files;
        # they are not this module's own SPDX tags (those are on lines 1-2).
        return [
            f"SPDX-FileCopyrightText: {COPYRIGHT_YEAR} {MAINTAINER} <{CONTACT}>",
            "SPDX-License-Identifier: GPL-3.0-or-later",
            # REUSE-IgnoreEnd
            "",
            f"{self.name} — {title}",
            "GENERATED by tools/steelbore_themes from Steelbore/steelbore.toml "
            f"(palette family v{self.family_version}, The Steelbore Standard §11 "
            f"v{self.standard_version}). Do not edit by hand — regenerate.",
            f"Theme slug: {self.slug} · palette: {self.palette_slug} · variant: {variant}",
            f"Conformance: {conformance}",
            f"Maintainer: {MAINTAINER} <{CONTACT}> · {PROJECT_URL}",
        ]

    def header(self, title: str, comment: str = "#") -> str:
        """Line-comment header (``#``, ``//``, ``--``, ``;``), newline-terminated."""
        return "".join(f"{comment}\n" if not line else f"{comment} {line}\n" for line in self.header_lines(title))

    def header_block(self, title: str, opener: str = "/*", closer: str = "*/") -> str:
        """Block-comment header (``/* */``, ``<!-- -->``), newline-terminated."""
        body = "\n".join(f" * {line}".rstrip() for line in self.header_lines(title))
        return f"{opener}\n{body}\n {closer}\n"


# -- colour helpers -------------------------------------------------------------


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """``#RRGGBB`` → ``(r, g, b)``.  Raises :class:`ValueError` for ANSI names."""
    if not _HEX_RE.match(value):
        msg = f"not a #RRGGBB colour: {value!r}"
        raise ValueError(msg)
    return (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16))


def relative_luminance(value: str) -> float:
    """WCAG 2.2 relative luminance of a ``#RRGGBB`` colour."""

    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = hex_to_rgb(value)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(a: str, b: str) -> float:
    """WCAG 2.2 contrast ratio between two ``#RRGGBB`` colours (``>= 1.0``)."""
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# -- loading --------------------------------------------------------------------


def _require_str(table: Mapping[str, object], key: str, where: str) -> str:
    value = table.get(key)
    if not isinstance(value, str):
        msg = f"{where}: expected string at {key!r}, got {type(value).__name__}"
        raise PaletteError(msg)
    return value


def _require_table(table: Mapping[str, object], key: str, where: str) -> Mapping[str, object]:
    value = table.get(key)
    if not isinstance(value, dict):
        msg = f"{where}: expected table at {key!r}"
        raise PaletteError(msg)
    return value


def _str_map(table: Mapping[str, object], where: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in table.items():
        if isinstance(value, str):
            out[key] = value
    if not out:
        msg = f"{where}: no string entries"
        raise PaletteError(msg)
    return out


def _classic_roles(six: Mapping[str, str]) -> dict[str, str]:
    """Fill the eleven-role contract from Classic's six roles.

    Fallbacks: ``surface``/``surface-alt`` → background (Classic defines no
    surface class, §11.2); ``structure``/``border`` → accent;
    ``warning`` → foreground (Molten Amber, the historical warning colour in
    this repository); ``focus`` → info (Liquid Coolant).  ``info`` is kept.
    """
    return {
        "background": six["background"],
        "surface": six["background"],
        "surface-alt": six["background"],
        "foreground": six["foreground"],
        "accent": six["accent"],
        "structure": six["accent"],
        "success": six["success"],
        "error": six["error"],
        "warning": six["foreground"],
        "focus": six["info"],
        "border": six["accent"],
        "info": six["info"],
    }


def _palette_slug_of(theme_slug: str) -> str:
    return theme_slug.removesuffix(_HC_SUFFIX)


def _kind_of(theme_slug: str) -> ThemeKind:
    if theme_slug == "steelbore-mono":
        return "mono"
    if theme_slug.endswith(_HC_SUFFIX):
        return "high-contrast"
    return "base"


def _conformance_of(palette_slug: str, fidelity: frozenset[str]) -> Conformance:
    if palette_slug == "steelbore-mono":
        return "mono"
    if palette_slug in fidelity:
        return "fidelity"
    if palette_slug == "steelbore-classic":
        return "legacy"
    return "conforming"


def _restricted_roles(rules: Mapping[str, object]) -> frozenset[str]:
    """Roles whose *-restriction* rule limits them to large text everywhere."""
    out: set[str] = set()
    for key in rules:
        if key.endswith("-restriction"):
            out.add(key.removesuffix("-restriction"))
    return frozenset(out)


def _non_role_fills(rules: Mapping[str, object]) -> tuple[str, ...]:
    out: list[str] = []
    for key in ("non-role-colors", "non-text-fill-only"):
        value = rules.get(key)
        if isinstance(value, list):
            out.extend(str(v).upper() for v in value)
    return tuple(out)


@dataclass(frozen=True, slots=True)
class Family:
    """The whole palette family as loaded from ``steelbore.toml``."""

    version: str
    standard_version: str
    default_theme: str
    default_light_theme: str
    registered_set: tuple[str, ...]
    themes: Mapping[str, Theme]
    pair: Mapping[str, str]
    env_var: str
    typography: Mapping[str, Mapping[str, str]]

    def __iter__(self) -> Iterator[Theme]:
        return iter(self.themes.values())

    def __getitem__(self, slug: str) -> Theme:
        return self.themes[slug]

    @property
    def default(self) -> Theme:
        return self.themes[self.default_theme]

    def ordered(self) -> tuple[Theme, ...]:
        """Every theme, default first, then the rest of the registered set in
        registration order, then Classic, then the fidelity pair.  Renderers
        that list themes (a VS Code ``package.json``) use this order so the
        default is always the first entry."""
        seen: list[str] = [self.default_theme]
        seen += [s for s in self.registered_set if s not in seen]
        seen += [s for s in self.themes if s not in seen]
        return tuple(self.themes[s] for s in seen)

    def hex_themes(self) -> tuple[Theme, ...]:
        """:meth:`ordered` without the mono variant."""
        return tuple(t for t in self.ordered() if not t.is_mono)


def _parse_standard_version(standard: str) -> str:
    match = re.search(r"v(\d+\.\d+)", standard)
    return match.group(1) if match else "unknown"


def load_family(toml_path: Path) -> Family:
    """Parse ``steelbore.toml`` into a :class:`Family`, validating its shape."""
    with toml_path.open("rb") as fh:
        raw = tomllib.load(fh)
    where = str(toml_path)
    meta = _require_table(raw, "meta", where)
    palettes = _require_table(raw, "palettes", where)
    themes_raw = _require_table(raw, "themes", where)
    resolution = _require_table(raw, "resolution", where)
    polarity_raw = _str_map(_require_table(resolution, "polarity", where), where)
    pair_raw = _str_map(_require_table(resolution, "pair", where), where)
    typography_raw = _require_table(raw, "typography", where)

    version = _require_str(meta, "version", where)
    standard_version = _parse_standard_version(_require_str(meta, "standard", where))
    fidelity_list = meta.get("fidelity-palettes")
    fidelity = frozenset(str(s) for s in fidelity_list) if isinstance(fidelity_list, list) else frozenset()
    registered_list = meta.get("registered-set")
    if not isinstance(registered_list, list):
        msg = f"{where}: [meta] registered-set missing"
        raise PaletteError(msg)
    registered = tuple(str(s) for s in registered_list)

    themes: dict[str, Theme] = {}
    for slug, table in themes_raw.items():
        if not isinstance(table, dict):
            continue
        kind = _kind_of(slug)
        palette_slug = _palette_slug_of(slug)
        palette_table = palettes.get(palette_slug)
        palette: dict[str, str] = {}
        if isinstance(palette_table, dict):
            palette = {k: v for k, v in _str_map(palette_table, where).items() if k != "reference"}
        roles_raw = {k: v for k, v in _str_map(table, where).items()}
        rules_raw = table.get("rules")
        rules: Mapping[str, object] = rules_raw if isinstance(rules_raw, dict) else {}
        contrast_raw = table.get("contrast")
        vs_bg: dict[str, str] = {}
        if isinstance(contrast_raw, dict):
            vs_bg_raw = contrast_raw.get("vs-background")
            if isinstance(vs_bg_raw, dict):
                vs_bg = {k: v for k, v in vs_bg_raw.items() if isinstance(v, str)}
        if palette_slug == "steelbore-classic":
            missing = [r for r in CLASSIC_ROLES if r not in roles_raw]
            if missing:
                msg = f"{where}: theme {slug} lacks classic roles {missing}"
                raise PaletteError(msg)
            roles = _classic_roles(roles_raw)
        else:
            if kind == "mono":
                # The mono variant declares no surface class; a surface fill in
                # 4-bit ANSI is simply the terminal's default background.
                roles_raw.setdefault("surface", "default")
                roles_raw.setdefault("surface-alt", "default")
            missing = [r for r in ROLES if r not in roles_raw]
            if missing:
                msg = f"{where}: theme {slug} lacks roles {missing}"
                raise PaletteError(msg)
            roles = {r: roles_raw[r] for r in ROLES}
        if kind != "mono":
            for role, value in roles.items():
                if not _HEX_RE.match(value):
                    msg = f"{where}: theme {slug} role {role} is not #RRGGBB: {value!r}"
                    raise PaletteError(msg)
        polarity_value = polarity_raw.get(palette_slug, "dark")
        polarity: Polarity = "light" if polarity_value == "light" else "dark"
        base_name = DISPLAY_NAMES.get(palette_slug, palette_slug)
        name = f"{base_name} High Contrast" if kind == "high-contrast" else base_name
        themes[slug] = Theme(
            slug=slug,
            name=name,
            palette_slug=palette_slug,
            palette_name=base_name,
            kind=kind,
            polarity=polarity,
            conformance=_conformance_of(palette_slug, fidelity),
            roles=roles,
            palette=palette,
            restricted_roles=_restricted_roles(rules),
            contrast_vs_background=vs_bg,
            non_role_fills=_non_role_fills(rules),
            family_version=version,
            standard_version=standard_version,
        )

    typography: dict[str, dict[str, str]] = {}
    for key in typography_raw:
        typography[key] = _str_map(_require_table(typography_raw, key, where), where)

    return Family(
        version=version,
        standard_version=standard_version,
        default_theme=_require_str(meta, "default-theme", where),
        default_light_theme=_require_str(meta, "default-light-theme", where),
        registered_set=registered,
        themes=themes,
        pair=pair_raw,
        env_var=_require_str(resolution, "env-var", where),
        typography=typography,
    )


def repo_root() -> Path:
    """The theme repository root (``tools/`` lives one level below it)."""
    return Path(__file__).resolve().parent.parent.parent


def default_toml_path() -> Path:
    return repo_root() / "Steelbore" / "steelbore.toml"
