# Steelbore Theme

**Canonical Spacecraft Software color theme — reference implementation of [The Steelbore Standard §9.1](https://Standard.SpacecraftSoftware.org/)**

`steelbore.json` is the authoritative token → hex + RGB mapping for the Steelbore
theme. All Spacecraft Software applications must expose palette colors through this
named theme rather than bare hex literals (Standard §9.1).

---

## Token reference

| Token        | Palette token  | Hex       | RGB                |
|--------------|----------------|-----------|--------------------|
| `background` | Void Navy      | `#000027` | RGB(0, 0, 39)      |
| `foreground` | Molten Amber   | `#D98E32` | RGB(217, 142, 50)  |
| `accent`     | Steel Blue     | `#4B7EB0` | RGB(75, 126, 176)  |
| `success`    | Radium Green   | `#50FA7B` | RGB(80, 250, 123)  |
| `error`      | Red Oxide      | `#FF5C5C` | RGB(255, 92, 92)   |
| `info`       | Liquid Coolant | `#8BE9FD` | RGB(139, 233, 253) |

---

## How to use

Copy `steelbore.json` into your project as its theme definition and reference tokens
by name in application logic. Never reference hex values directly in UI code.

**Examples by platform:**

| Platform | Convention |
|----------|------------|
| JSON config | `"themes/steelbore.json"` — copy file, reference tokens by key |
| TOML config | `steelbore.toml` — translate tokens to your config format |
| Rust (ratatui / iced) | `enum Theme { Steelbore }` → `impl Theme { fn background(&self) -> Color }` |
| CSS | `@import "steelbore.css"` with `var(--background)`, `var(--foreground)`, … |
| TypeScript | `import steelbore from "./steelbore.json"` → `steelbore.tokens.background.hex` |

The theme **must** be registered under the name `steelbore` (snake_case) in the
project's theme registry or configuration layer.

---

## Normative rule

> Hard-coding palette hex values directly in UI logic is **forbidden** for new
> Spacecraft Software apps. Use theme tokens exclusively.
> — The Steelbore Standard §9.1

See <https://Standard.SpacecraftSoftware.org/> for the full normative text.

---

**License:** GPL-3.0-or-later  
**Copyright:** Copyright (C) 2026 Mohamed Hammad & Spacecraft Software
