# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Deterministic archive builder.

Rebuilds every :class:`Archive` a target declares from the generated tree.
Timestamps are pinned and entries are sorted so a rebuild from an unchanged
tree is byte-identical, which keeps ``git status`` honest.
"""

from __future__ import annotations

import io
import tarfile
import zipfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from steelbore_themes.renderers import Archive

_EPOCH_ZIP: tuple[int, int, int, int, int, int] = (2026, 1, 1, 0, 0, 0)
_EPOCH_TAR: int = 1767225600  # 2026-01-01T00:00:00Z


def _walk(source: Path, dest: str) -> Iterator[tuple[Path, str]]:
    if source.is_file():
        yield source, dest
        return
    for child in sorted(source.rglob("*")):
        if child.is_file():
            rel = child.relative_to(source).as_posix()
            yield child, f"{dest}/{rel}" if dest else rel


def _entries(target_dir: Path, archive: Archive) -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    for src, dst in archive.entries:
        source = target_dir / src
        if not source.exists():
            msg = f"{archive.path}: missing source {source}"
            raise FileNotFoundError(msg)
        out.extend(_walk(source, dst))
    return sorted(out, key=lambda e: e[1])


def _write_zip(entries: list[tuple[Path, str]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for source, name in entries:
            info = zipfile.ZipInfo(name, date_time=_EPOCH_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, source.read_bytes())
    return buffer.getvalue()


def _write_tar_gz(entries: list[tuple[Path, str]]) -> bytes:
    buffer = io.BytesIO()
    # mtime=0 on the gzip header keeps the stream deterministic.
    with (
        io.BytesIO() as raw,
        tarfile.open(fileobj=raw, mode="w") as tf,
    ):
        for source, name in entries:
            data = source.read_bytes()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = _EPOCH_TAR
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tf.addfile(info, io.BytesIO(data))
        tf.close()
        import gzip

        with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as gz:
            gz.write(raw.getvalue())
    return buffer.getvalue()


def build_archive(root: Path, target_dir: str, archive: Archive) -> Path:
    """Build one archive and return its path.  Overwrites in place."""
    entries = _entries(root / target_dir, archive)
    payload = _write_tar_gz(entries) if archive.fmt == "tar.gz" else _write_zip(entries)
    out = root / archive.path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(payload)
    return out
