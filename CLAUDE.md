# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Code

**Python script:**
```
python hello.py
```
No dependencies required. The script uses `sys.stdout` with UTF-8 encoding to print Thai text.

**HTML game:**
Open `whac-a-mole.html` directly in a browser — no server needed.

## Project Overview

Two standalone files, no build process, no package manager, no external dependencies.

- `hello.py` — Hello World in Thai (สวัสดีโลก), demonstrates UTF-8 output on Windows via `sys.stdout`.
- `whac-a-mole.html` — Self-contained Whac-A-Mole game (เกมตีตัวตุ่น) in Thai. All CSS and JavaScript are inlined. Game logic includes a 3×3 mole grid, three difficulty levels, a 30-second timer, score/miss tracking, and end-of-game grading. No external assets or libraries.
