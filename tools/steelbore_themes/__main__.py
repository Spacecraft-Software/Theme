# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Command-line entry point.

    cd tools && python3 -m steelbore_themes list
    cd tools && python3 -m steelbore_themes generate [--target ID ...] [--clean] [--dry-run]
    cd tools && python3 -m steelbore_themes validate [--target ID ...]
    cd tools && python3 -m steelbore_themes package  [--target ID ...]
    cd tools && python3 -m steelbore_themes registry

Diagnostics go to stderr with a severity tag; results go to stdout.  Exit 0 on
success, 1 on a validation failure, 2 on a usage or I/O error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from steelbore_themes.core import (
    ANSI_SLOTS,
    ROLES,
    Family,
    PaletteError,
    Theme,
    default_toml_path,
    load_family,
    repo_root,
)
from steelbore_themes.package import build_archive
from steelbore_themes.renderers import Archive, Target, discover
from steelbore_themes.validate import Finding, check_bundle_files, check_theme_files

if TYPE_CHECKING:
    from collections.abc import Sequence


def _info(msg: str) -> None:
    print(f"[INFO] {msg}", file=sys.stderr)


def _warn(msg: str) -> None:
    print(f"[WARN] {msg}", file=sys.stderr)


def _error(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)


def _select(targets: dict[str, Target], wanted: Sequence[str] | None) -> list[Target]:
    if not wanted:
        return list(targets.values())
    missing = [w for w in wanted if w not in targets]
    if missing:
        names = ", ".join(missing)
        msg = f"unknown target(s): {names}; run `list` (a failed import is reported above)"
        raise SystemExit(f"[ERROR] {msg}")
    return [targets[w] for w in wanted]


def _themes_for(family: Family, target: Target) -> tuple[Theme, ...]:
    out: list[Theme] = []
    for theme in family.ordered():
        if theme.is_mono and not target.supports_mono:
            continue
        if theme.slug in target.extra_skip:
            continue
        out.append(theme)
    return tuple(out)


def _render_target(family: Family, target: Target) -> tuple[dict[str, str], list[Finding]]:
    """Render every theme for one target.  Returns ``(files, findings)`` where
    file paths are relative to the repository root."""
    files: dict[str, str] = {}
    findings: list[Finding] = []
    themes = _themes_for(family, target)
    for theme in themes:
        rendered = dict(target.render(theme))
        findings.extend(Finding(f"{target.target_dir}/{f.path}", f.message) for f in check_theme_files(theme, rendered))
        for rel, content in rendered.items():
            full = f"{target.target_dir}/{rel}"
            if full in files:
                findings.append(Finding(full, f"emitted twice (theme {theme.slug})"))
            files[full] = content
    if target.render_bundle is not None:
        bundle = dict(target.render_bundle(themes))
        allowed = frozenset().union(*(t.allowed_hexes() for t in themes))
        findings.extend(
            Finding(f"{target.target_dir}/{f.path}", f.message) for f in check_bundle_files(bundle, allowed)
        )
        for rel, content in bundle.items():
            full = f"{target.target_dir}/{rel}"
            if full in files:
                findings.append(Finding(full, "bundle file collides with a theme file"))
            files[full] = content
    return files, findings


def cmd_list(family: Family, targets: dict[str, Target], args: argparse.Namespace) -> int:
    if args.json:
        payload = {
            "targets": [
                {
                    "id": t.id,
                    "target_dir": t.target_dir,
                    "supports_mono": t.supports_mono,
                    "archives": [a.path for a in t.archives],
                    "description": t.description,
                }
                for t in targets.values()
            ],
            "themes": [t.slug for t in family.ordered()],
        }
        print(json.dumps(payload, indent=2))
        return 0
    print(f"{len(family.themes)} themes; {len(targets)} targets")
    for target in targets.values():
        mono = "mono" if target.supports_mono else "hex-only"
        print(f"  {target.id:<22} {target.target_dir:<42} {mono}")
    return 0


def cmd_generate(family: Family, targets: dict[str, Target], args: argparse.Namespace) -> int:
    root = repo_root()
    selected = _select(targets, args.target)
    all_findings: list[Finding] = []
    written = 0
    for target in selected:
        files, findings = _render_target(family, target)
        all_findings.extend(findings)
        if findings and not args.force:
            _warn(f"{target.id}: {len(findings)} finding(s); not writing (use --force)")
            continue
        if args.clean:
            for legacy in target.legacy_files:
                path = root / target.target_dir / legacy
                if path.exists():
                    if args.dry_run:
                        _info(f"would remove {path.relative_to(root)}")
                    else:
                        path.unlink()
                        _info(f"removed legacy {path.relative_to(root)}")
        for rel, content in sorted(files.items()):
            path = root / rel
            if args.dry_run:
                print(rel)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.read_text(encoding="utf-8") == content:
                continue
            path.write_text(content, encoding="utf-8", newline="\n")
            written += 1
        _info(f"{target.id}: {len(files)} file(s)")
    for finding in all_findings:
        _error(str(finding))
    if not args.dry_run:
        _info(f"wrote {written} changed file(s)")
    return 1 if all_findings else 0


def cmd_validate(family: Family, targets: dict[str, Target], args: argparse.Namespace) -> int:
    root = repo_root()
    selected = _select(targets, args.target)
    total = 0
    stale = 0
    for target in selected:
        files, findings = _render_target(family, target)
        for finding in findings:
            _error(str(finding))
        total += len(findings)
        for rel, content in files.items():
            path = root / rel
            if not path.exists():
                _error(f"{rel}: missing on disk (run generate)")
                stale += 1
            elif path.read_text(encoding="utf-8") != content:
                _error(f"{rel}: differs from generator output (run generate)")
                stale += 1
    if total == 0 and stale == 0:
        print(f"[OK] {len(selected)} target(s) valid and up to date")
        return 0
    print(f"[ERROR] {total} finding(s), {stale} stale file(s)")
    return 1


def _expand_archive(archive: Archive, themes: Sequence[Theme]) -> list[Archive]:
    if not archive.per_theme:
        return [archive]
    out: list[Archive] = []
    for theme in themes:
        out.append(
            Archive(
                path=archive.path.replace("{slug}", theme.slug),
                fmt=archive.fmt,
                entries=tuple(
                    (src.replace("{slug}", theme.slug), dst.replace("{slug}", theme.slug))
                    for src, dst in archive.entries
                ),
            )
        )
    return out


def cmd_package(family: Family, targets: dict[str, Target], args: argparse.Namespace) -> int:
    root = repo_root()
    selected = _select(targets, args.target)
    built = 0
    for target in selected:
        for archive in target.archives:
            expanded = _expand_archive(archive, _themes_for(family, target))
            for concrete in expanded:
                try:
                    build_archive(root, target.target_dir, concrete)
                except FileNotFoundError as exc:
                    _error(str(exc))
                    return 2
                built += 1
            _info(f"{target.id}: built {len(expanded)} archive(s) for {archive.path}")
    print(f"[OK] built {built} archive(s)")
    return 0


def cmd_registry(family: Family, targets: dict[str, Target], args: argparse.Namespace) -> int:
    """Write ``Steelbore/steelbore.json`` — the family as a JSON registry."""
    root = repo_root()
    payload: dict[str, object] = {
        "name": "Steelbore",
        "description": (
            "Spacecraft Software palette family registry — The Steelbore Standard §11. "
            "GENERATED from Steelbore/steelbore.toml by tools/steelbore_themes; do not edit."
        ),
        "family-version": family.version,
        "standard": f"The Steelbore Standard §11 (v{family.standard_version})",
        "spdx-license-identifier": "GPL-3.0-or-later",
        "copyright": "Copyright (C) 2026 Mohamed Hammad & Spacecraft Software",
        "source": "https://Standard.SpacecraftSoftware.org/",
        "default-theme": family.default_theme,
        "default-light-theme": family.default_light_theme,
        "env-var": family.env_var,
        "registered-set": list(family.registered_set),
        "roles": list(ROLES),
        "ansi-slots": list(ANSI_SLOTS),
        "typography": {k: dict(v) for k, v in family.typography.items()},
        "themes": {
            theme.slug: {
                "name": theme.name,
                "palette": theme.palette_slug,
                "variant": theme.kind,
                "polarity": theme.polarity,
                "conformance": theme.conformance,
                "pair": family.pair.get(theme.palette_slug),
                "roles": dict(theme.roles),
                "ansi": list(theme.ansi16()),
                "contrast-vs-background": dict(theme.contrast_vs_background),
                "restricted-roles": sorted(theme.restricted_roles),
            }
            for theme in family.ordered()
        },
    }
    out = root / "Steelbore" / "steelbore.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"[OK] wrote {out.relative_to(root)}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="steelbore_themes", description=__doc__)
    parser.add_argument("--toml", type=Path, default=default_toml_path())
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list targets and themes")
    p_list.add_argument("--json", action="store_true")

    p_gen = sub.add_parser("generate", help="render themes to the repository")
    p_gen.add_argument("--target", action="append")
    p_gen.add_argument("--clean", action="store_true", help="delete legacy hand-written files")
    p_gen.add_argument("--dry-run", action="store_true")
    p_gen.add_argument("--force", action="store_true", help="write even with findings")

    p_val = sub.add_parser("validate", help="re-render and compare with disk")
    p_val.add_argument("--target", action="append")

    p_pkg = sub.add_parser("package", help="rebuild declared archives")
    p_pkg.add_argument("--target", action="append")

    sub.add_parser("registry", help="write Steelbore/steelbore.json")

    args = parser.parse_args(argv)
    try:
        family = load_family(args.toml)
    except (OSError, PaletteError) as exc:
        _error(f"cannot load palette family: {exc}")
        return 2
    failures: dict[str, str] = {}
    targets = discover(failures)
    for module, error in failures.items():
        _warn(f"renderer module {module!r} failed to import: {error}")
    commands = {
        "list": cmd_list,
        "generate": cmd_generate,
        "validate": cmd_validate,
        "package": cmd_package,
        "registry": cmd_registry,
    }
    return commands[args.command](family, targets, args)


if __name__ == "__main__":
    sys.exit(main())
