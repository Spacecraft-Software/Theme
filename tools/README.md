<!--
SPDX-FileCopyrightText: 2026 Mohamed Hammad <Mohamed.Hammad@SpacecraftSoftware.org>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# `tools/steelbore_themes` — the theme generator

Every theme file under `Editors/`, `Terminals/`, `Desktops/`, `Shells/`,
`Browsers/`, `CLIs/`, `Bootloaders/` and `Steelbore/` is **generated** from one
source, `Steelbore/steelbore.toml` — a verbatim copy of the canonical palette
contract shipped by the `steelbore-color-palette` skill (The Steelbore Standard
§11, palette family v3.5.0, Standard v2.08). Never edit a generated file; edit
the renderer (or the TOML upstream) and regenerate.

```sh
cd tools
python3 -m steelbore_themes list                 # targets and themes
python3 -m steelbore_themes generate             # render everything
python3 -m steelbore_themes generate --target kitty --clean   # one target; delete its legacy files
python3 -m steelbore_themes validate             # re-render and diff against disk
python3 -m steelbore_themes package              # rebuild every declared archive
python3 -m steelbore_themes registry             # rewrite Steelbore/steelbore.json
```

Plain `python3` ≥ 3.11, no dependencies (`tomllib` is stdlib). Diagnostics go
to stderr tagged `[INFO]` / `[WARN]` / `[ERROR]`; exit 1 on a finding.

## What gets generated

For every target, one file (or one directory) per theme under
`<target>/themes/`, named by the theme **slug**:

| Slug | Name | Variant | Canvas polarity |
|------|------|---------|-----------------|
| `steelbore` | Steelbore | **default** (Modern) | dark |
| `steelbore-high-contrast` | Steelbore High Contrast | §11.1.1 sibling | dark |
| `steelbore-blue`, `-high-contrast` | Steelbore Blue | alternate §11.3.1 | dark |
| `steelbore-magnetar`, `-high-contrast` | Steelbore Magnetar | alternate §11.3.2 | dark |
| `steelbore-biolume`, `-high-contrast` | Steelbore Biolume | alternate §11.3.3 | dark |
| `steelbore-navywhite`, `-high-contrast` | Steelbore NavyWhite | alternate §11.3.4 | **light** |
| `tokyonight`, `-high-contrast` | Tokyo Night | alternate §11.3.5 | dark |
| `steelbore-hanzosteel`, `-high-contrast` | Steelbore Hanzo Steel | alternate §11.3.6 | dark |
| `steelbore-blackpinkpanther`, `-high-contrast` | Steelbore BlackPinkPanther | alternate §11.3.7 | dark |
| `steelbore-green`, `-high-contrast` | Steelbore Green | alternate §11.3.8 | dark |
| `steelbore-greenalt`, `-high-contrast` | Steelbore Green Alt | alternate §11.3.9 | dark |
| `steelbore-classic`, `-high-contrast` | Steelbore Classic | legacy six-role §11.2 | dark |
| `solarized-dark`, `solarized-light` | Solarized | **fidelity §11.5, non-conforming** | dark / light |
| `steelbore-mono` | Steelbore Mono | 4-bit ANSI, `NO_COLOR` | — |

That is 24 hex themes, plus mono where the format can express ANSI names.
`steelbore` is always the default and always listed first.

## Writing a renderer

One module per platform in `steelbore_themes/renderers/`. Copy `kitty.py`.
The module exposes `TARGET: Target` (or `TARGETS: tuple[Target, ...]` when one
format serves several vendor directories — Chromium browsers, JetBrains IDEs).

```python
def render(theme: Theme) -> Mapping[str, str]:      # one theme → {relpath: text}
def render_bundle(themes: Sequence[Theme]) -> Mapping[str, str]:  # optional, once
TARGET = Target(id=..., target_dir=..., render=render, supports_mono=...,
                render_bundle=..., legacy_files=(...), archives=(...))
```

Rules, in priority order:

1. **No hex literal anywhere in a renderer.** Every colour is
   `theme.<role>`, `theme.palette["Named Colour"]`, `theme.ansi[...]`,
   `theme.with_alpha(role, "40")`, `theme.rgb(role)`, `theme.rgb_float(role)`
   or `theme.hex_bare(role)`. The validator rejects any `#RRGGBB` in the output
   that is not that theme's own palette, any lifted (`* Lift`) hex outside a
   high-contrast variant, and every pre-generator legacy colour (`#050530`,
   `#6272A4`, `#E6E6F0`, `#BD93F9`, `#FE6B00`, `#0E141D`, `#142E46`, `#F0F0F0`,
   the Dracula-derived bright ANSI set, …).
2. **Role semantics** (§11.1). Map the platform's keys onto these meanings and
   nothing else:

   | Role | Meaning in a UI | Typical keys |
   |------|-----------------|--------------|
   | `background` | the canvas — editor, terminal, window, page | `editor.background`, `bg_color`, `window_bg_color` |
   | `surface` | elevated panels, sidebars, cards, tab bars, popovers, current line | `sideBar.background`, `card_bg_color`, `panel.background` |
   | `surface-alt` | code blocks, terminal wells, input fields, gutters | `input.background`, `terminal.background` inside an editor |
   | `foreground` | body text, default readout, cursor | `editor.foreground`, `text`, `fg_color` |
   | `accent` | primary accent: active tab underline, buttons, keywords, selection fill | `activityBarBadge`, `accent_color`, `keyword` |
   | `structure` | links, borders, comments/dim text, line numbers, secondary text, types | `editorLineNumber`, `Link`, `comment`, `border` |
   | `success` | success state, strings, git added | `gitDecoration.addedResourceForeground`, `string` |
   | `error` | error state, deletions, invalid | `errorForeground`, `destructive_color` |
   | `warning` | warning / attention, numbers & constants, modified | `editorWarning`, `warning_color`, `constant.numeric` |
   | `focus` | focus ring, cursor of the active pane, functions | `focusBorder`, `editorCursor`, `function` |
   | `border` | structural borders (an alias of `structure` in every palette) | `border`, `split` |

   Any "muted / disabled / placeholder" key takes `structure`, never a surface
   token — **surface tokens are fills only, never text** (§11.0.1).
3. **Text on fills.** A foreground role on `background`, `surface` or
   `surface-alt` is a verified pairing in every conforming palette. Text of one
   foreground role on top of another foreground role is *not* verified and
   mostly fails; the only allowed inversion is `background` text on an
   `accent`/`structure`/`success`/`error` fill (selected tab, primary button),
   which is the same pair measured the other way round.
4. **Restricted accents.** `theme.text_safe_accent` is `accent` except where the
   palette restricts it to large text (Steelbore Blue: Electric Blue, 3.91:1);
   use it for any *normal-size text* slot. Plain `theme.accent` is fine for
   fills, borders, icons and large text.
5. **Translucent fills** (selection, hover, match highlight) use
   `theme.with_alpha(role, "40")` — palette hex plus alpha, fills only.
6. **Classic** binds six roles; `theme.surface`, `surface_alt` resolve to the
   canvas, `structure`/`border` to the accent, `warning` to the foreground,
   `focus` to `info`. `theme.info` exists on every theme (Classic's Liquid
   Coolant; `structure` elsewhere). Nothing special to do.
7. **Mono.** If the format takes ANSI colour *names* or 4-bit codes (shell
   prompts, Starship, TTY), set `supports_mono=True` and branch on
   `theme.is_mono`: `theme.roles[...]` then holds `"red"`, `"bright-white"`,
   `"default"`, `"reverse-video"`; `theme.ansi[slot]` holds the slot name.
   Hex-only formats leave it `False` and the generator skips mono for them.
8. **Light canvas.** `steelbore-navywhite` and `solarized-light` are light;
   set the platform's `dark`/`light` flag from `theme.is_dark`, never hardcode.
9. **Header.** Text formats that allow comments start with
   `theme.header("Platform theme")` (line comments) or
   `theme.header_block(...)` (`/* */`, `<!-- -->`). Pure JSON gets no header —
   REUSE coverage for JSON comes from the repo-root `REUSE.toml`.
10. **ANSI 16.** `theme.ansi` / `theme.ansi_bright` / `theme.ansi16()` are the
    only ANSI mapping (black=background, red=error, green=success,
    yellow=warning, blue=structure, magenta=accent (text-safe), cyan=focus,
    white=foreground; bright = same, bright-black=structure). Never re-derive.
11. **Fonts** (§12): where a format names a font, `Inconsolata` for body /
    monospace with `Share Tech Mono` for headings, `monospace` fallback.
    Nothing else — no JetBrains Mono, Consolas, Outfit, Roboto.
12. **Text hygiene** (§6.5): LF, UTF-8, final newline. Build content with
    `"\n".join(lines) + "\n"` or `json.dumps(..., indent=2) + "\n"`.
13. **`legacy_files`** lists the hand-written pre-generator files the target
    replaces (relative to `target_dir`); `generate --clean` deletes them.
    Binary assets (PNG, `.themepack`) are never listed.
14. **`archives`** re-declare the target's existing shippable archive by its
    existing path so links keep working; contents are `themes/` plus
    `INSTALL.md` (plus package files for extensions). Image assets are not
    archived.
15. **`INSTALL.md`** in the target directory is hand-written (not generated):
    keep its header line, replace the single-file instructions with the
    `themes/<slug>.<ext>` layout, name `steelbore` as the default, mention the
    `-high-contrast` siblings, note that Solarized is a non-conforming fidelity
    palette, and add a short "Choosing a theme" table or the env var
    `SPACECRAFT_THEME=<slug>` where the platform can read it.

Validate with `python3 -m steelbore_themes generate --target <id> --clean`
(exit 0, no `[ERROR]`), then eyeball one dark, one high-contrast, `navywhite`
(light) and `solarized-light` output.
