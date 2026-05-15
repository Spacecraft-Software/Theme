---
name: spacecraft-theme-factory
description: A specialized tool for generating high-quality Spacecraft Software-compliant themes for various IDEs, editors, and terminal environments. Use it when you need to extend Spacecraft Software support to a new platform.
license: GPL-3.0-or-later
---

# Spacecraft Software Theme Factory

## Overview

The Theme Factory is the central engine for creating and refining Spacecraft Software themes. It ensures that every extension follows the "Spacecraft Software Standard" for visual excellence.

**Keywords**: theme generation, IDE themes, editor colors, UI design, Spacecraft Software standard, palette consistency, visual design factory

## Core Spacecraft Software Palette

- **Background**: `#000027` (Midnight Navy)
- **Foreground**: `#F0F0F0` (Off-White)
- **Accent (Primary)**: `#FE6B00` (Steel Orange)
- **Accent (Secondary)**: `#3B82F6` (Steel Blue)
- **Status/String**: `#10B981` (Steel Green)
- **Secondary BG**: `#142E46` (Bright Black/Navy)

## Usage

1. **Select a Target**: Identify the platform (e.g., VS Code, JetBrains, Terminal).
2. **Apply Standards**: Refer to `Spacecraft-Software-brand-guidelines` for typography and spacing.
3. **Generate Assets**: Use the defined palette to create configuration files (JSON, XML, etc.).
4. **Validation**: Each theme must be WOW-worthy and premium before versioning.

## Directory Structure

- `/themes`: Source definitions for different implementations.
- `/scripts`: (Future) Automation scripts for theme generation.
- `/templates`: Boilerplates for common IDE formats.

## Features

- **Palette Syncing**: Ensures all generated themes use identical hex codes.
- **Premium Aesthetics**: Enforces modern typography (Outfit/Roboto) and high-contrast accessibility.
- **Multi-Platform Support**: Extensible to any terminal or GUI application.
- **Document Output**: For DOCX and PDF, forces `#000027` page background and ISO A4 (210 × 297 mm) page size.
