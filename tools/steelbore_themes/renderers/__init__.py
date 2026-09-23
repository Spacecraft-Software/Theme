# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Renderer registry.

A renderer is one module in this package that translates a :class:`Theme` into
one platform's native theme format.  Each module exposes a single
:data:`TARGET` of type :class:`Target`; the registry discovers every module at
import time, so adding a platform is adding a file.

Contract (read this before writing a renderer):

* ``render(theme)`` returns ``{relative_path: content}`` for **one** theme.
  Paths are relative to ``target_dir`` and by convention live under
  ``themes/`` (``themes/<slug>.conf``, or ``themes/<slug>/gtk.css`` for
  multi-file bundles).  Content is text, LF-terminated, ending in a newline.
* ``render_bundle(themes)`` (optional) returns package-level files that list
  every theme — a VS Code ``package.json``, a JetBrains ``plugin.xml``, a
  Windows Terminal ``schemes.json``.  It is called once with the themes the
  target supports, default first (:meth:`Family.ordered`).
* ``supports_mono`` says whether ``steelbore-mono`` (ANSI names, no hexes) can
  be expressed in this format.  Hex-only formats set it ``False`` and the
  generator skips the mono theme for them.
* ``legacy_files`` names the pre-generator hand-written files that the
  generated output replaces; ``generate --clean`` deletes them.
* ``archives`` declares the shippable archives rebuilt by ``package``.
* Every colour comes from the :class:`Theme` — a renderer never contains a hex
  literal.  Translucent fills use ``theme.with_alpha(role, "40")``.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

from steelbore_themes.core import Theme

RenderFn = Callable[[Theme], Mapping[str, str]]
BundleFn = Callable[[Sequence[Theme]], Mapping[str, str]]
ArchiveFormat = Literal["zip", "tar.gz", "xpi", "vsix"]


@dataclass(frozen=True, slots=True)
class Archive:
    """One shippable archive.

    ``path`` is repo-relative.  ``entries`` maps a source (file or directory,
    relative to the target directory) to its path inside the archive; a
    directory is added recursively.  ``xpi`` and ``vsix`` are zip containers
    with a different extension — the renderer supplies any manifest files the
    container needs through ``render_bundle``.
    """

    path: str
    fmt: ArchiveFormat
    entries: tuple[tuple[str, str], ...]
    per_theme: bool = False
    """When true, ``{slug}`` in ``path`` and ``entries`` is expanded once per
    theme the target renders, producing one archive per theme — for formats
    whose installer takes exactly one theme per container (a Firefox ``.xpi``,
    a Chrome theme ``.zip``)."""


@dataclass(frozen=True, slots=True)
class Target:
    """A platform target: where its files go and how to render them."""

    id: str
    target_dir: str
    render: RenderFn
    supports_mono: bool = False
    render_bundle: BundleFn | None = None
    legacy_files: tuple[str, ...] = ()
    archives: tuple[Archive, ...] = ()
    description: str = ""
    extra_skip: frozenset[str] = field(default_factory=frozenset)
    """Theme slugs this target cannot express besides mono (rare)."""


class DiscoveryError(ImportError):
    """A renderer module failed to import; carried, not raised, by discover()."""


def discover(failures: dict[str, str] | None = None) -> dict[str, Target]:
    """Import every renderer module and collect its ``TARGET`` (or ``TARGETS``).

    A module that fails to import is skipped and recorded in ``failures``
    (``module name -> error``) so one broken renderer never blocks the others;
    the CLI reports the failure and errors only if that target was requested.
    """
    targets: dict[str, Target] = {}
    package_path = __path__
    for info in sorted(pkgutil.iter_modules(package_path), key=lambda m: m.name):
        if info.name.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"{__name__}.{info.name}")
        except Exception as exc:  # any import-time error is a discovery failure
            if failures is not None:
                failures[info.name] = f"{type(exc).__name__}: {exc}"
            continue
        found: list[Target] = []
        single = getattr(module, "TARGET", None)
        if isinstance(single, Target):
            found.append(single)
        many = getattr(module, "TARGETS", None)
        if isinstance(many, (tuple, list)):
            found.extend(t for t in many if isinstance(t, Target))
        if not found:
            if failures is not None:
                failures[info.name] = "module defines neither TARGET nor TARGETS"
            continue
        for target in found:
            if target.id in targets:
                msg = f"duplicate renderer id {target.id!r} in module {info.name}"
                raise ValueError(msg)
            targets[target.id] = target
    return targets
