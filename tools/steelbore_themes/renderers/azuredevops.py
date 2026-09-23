# SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Azure DevOps web theme extension.

Renders each theme as a single ``ms.vss-web.theme`` contribution
(``themes/<slug>.json``) plus a ``vss-extension.json`` bundle that lists one
contribution per theme, ready for ``tfx extension create``. Pure JSON — no
header, per §5.7/§9 rule 9 (REUSE coverage for JSON comes from the
repo-root ``REUSE.toml``).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from steelbore_themes.renderers import Archive, Target

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from steelbore_themes.core import Theme

_PUBLISHER = "Spacecraft-Software"
_EXTENSION_ID = "spacecraft-software-theme"
_EXTENSION_VERSION = "2.0.0"


def _contribution(theme: Theme) -> dict[str, object]:
    """The single ``ms.vss-web.theme`` contribution object for one theme.

    Key mapping (tools/README.md rule 2): background/foreground are the
    canvas and its text; secondary-text-color and link-color take
    ``structure`` (secondary text, links); the primary button is an
    ``accent`` fill with ``background`` text on top of it — the one verified
    foreground-on-foreground inversion (rule 3); card/input backgrounds are
    fills, so they take ``surface``/``surface-alt``, never a text role.
    """
    return {
        "id": f"spacecraft-software-{theme.slug}-theme",
        "type": "ms.vss-web.theme",
        "description": f"{theme.name} theme for Azure DevOps",
        "targets": ["ms.vss-web.theme-collection"],
        "properties": {
            "name": theme.name,
            "uiTheme": "light" if theme.is_light else "dark",
            "variables": {
                "background-color": theme.background,
                "primary-text-color": theme.foreground,
                "secondary-text-color": theme.structure,
                "primary-button-background": theme.accent,
                "primary-button-text": theme.background,
                "accent-color": theme.accent,
                "error-color": theme.error,
                "success-color": theme.success,
                "warning-color": theme.warning,
                "link-color": theme.structure,
                "border-color": theme.border,
                "card-background": theme.surface,
                "input-background": theme.surface_alt,
            },
        },
    }


def render(theme: Theme) -> Mapping[str, str]:
    """One ``themes/<slug>.json`` per theme: the bare contribution object."""
    return {f"themes/{theme.slug}.json": json.dumps(_contribution(theme), indent=2) + "\n"}


def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:
    """``vss-extension.json`` — the full manifest, one contribution per theme."""
    manifest: dict[str, object] = {
        "manifestVersion": 1,
        "id": _EXTENSION_ID,
        "version": _EXTENSION_VERSION,
        "name": "Spacecraft Software Theme",
        "description": "The Steelbore palette family for Azure DevOps boards and pipelines.",
        "publisher": _PUBLISHER,
        "icons": {"default": "icon.png"},
        "links": {"home": {"uri": "https://SpacecraftSoftware.org"}},
        "categories": ["Azure Pipelines", "Azure Boards"],
        "targets": [{"id": "Microsoft.VisualStudio.Services"}],
        "contributions": [_contribution(theme) for theme in themes],
        "files": [{"path": "icon.png", "addressable": True}],
    }
    return {"vss-extension.json": json.dumps(manifest, indent=2) + "\n"}


TARGET = Target(
    id="azuredevops",
    target_dir="Editors/AzureDevOps",
    render=render,
    render_bundle=render_bundle,
    supports_mono=False,
    legacy_files=("SpacecraftSoftware.spacecraft-software-theme-1.0.0.vsix",),
    archives=(
        Archive(
            path="Editors/AzureDevOps/spacecraft-software-azuredevops-theme.zip",
            fmt="zip",
            entries=(
                ("vss-extension.json", "vss-extension.json"),
                ("themes", "themes"),
                ("LICENSE", "LICENSE"),
                ("README.md", "README.md"),
                ("INSTALL.md", "INSTALL.md"),
            ),
        ),
        Archive(
            path="Editors/AzureDevOps/SpacecraftSoftware.spacecraft-software-theme-2.0.0.vsix",
            fmt="vsix",
            entries=(
                ("vss-extension.json", "vss-extension.json"),
                ("themes", "themes"),
                ("LICENSE", "LICENSE"),
                ("README.md", "README.md"),
            ),
        ),
    ),
    description="Azure DevOps web theme extension (themes/<slug>.json + vss-extension.json bundle)",
)
