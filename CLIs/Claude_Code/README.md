# Spacecraft Software for Claude Code

Elegant dark theme with high contrast and vivid accents, optimized for Claude Code.

## 🎨 Palette

- **Background**: `#0E141D` (Deep Navy)
- **Foreground**: `#F0F0F0` (Off-White)
- **Accent**: `#FE6B00` (Steel Orange)

## 🚀 Installation

### 1. Terminal Setup (Windows Terminal)
1. Open Windows Terminal **Settings**.
2. Go to **Color schemes** > **Add new**.
3. Copy the contents of [`spacecraft-software-terminal.json`](./spacecraft-software-terminal.json) into the configuration.
4. Set **Spacecraft Software** as your active scheme for the profile you use with Claude Code.

### 2. Claude Code Setup
To configure the custom status line and ensure colors display correctly:

1. Open (or create) `%USERPROFILE%\.claude\settings.json`.
2. Merge the configuration from [`settings.json`](./settings.json).
3. If colors look "washed out", ensure your environment variable `COLORTERM=truecolor` is set.

## 📊 Status Line
The included configuration adds a Spacecraft-Software-themed status line that shows:
- **Model Name** (in Spacecraft Software Orange)
- **Context Usage** (in Spacecraft Software Blue)
