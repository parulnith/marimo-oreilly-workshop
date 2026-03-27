# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational workshop teaching the modern AI/ML development stack using **marimo**, a reactive Python notebook framework. The curriculum is organized into 5 modules (Modules 2, 4, 5 are still in development):

- **Module 1**: Interactive environments foundations — why notebooks matter, their limitations, reactive execution
- **Module 2**: Reproducibility and trustworthiness in AI (planned)
- **Module 3**: Interactivity accelerating AI discovery — ML classification demos
- **Module 4**: AI coding agents for development (planned)
- **Module 5**: Converting interactive work into reusable systems (planned)

## Running Marimo Apps

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run a marimo app (viewer mode)
marimo run Module_1/1.3.py

# Edit a marimo app (editor mode)
marimo edit Module_1/1.3.py
```

## Key Conventions

- **Python 3.13** with virtual environment at `.venv/`
- **Black** formatter with format-on-save enabled
- Marimo Python files use **PEP 723 inline script metadata** for dependencies:
  ```python
  # /// script
  # dependencies = ["marimo", "matplotlib", "pandas"]
  # requires-python = ">=3.13"
  # ///
  ```
- No requirements.txt or pyproject.toml — dependencies are declared per-script via PEP 723

## Content Guidelines

**Always follow the booklet strictly.** When creating or updating slides, notebooks, or any workshop content, the source of truth is `booklet_complete.md`. Do not invent examples, add steps, or deviate from the booklet's wording, code, or structure. If the booklet specifies exact code, use it verbatim.

## Architecture

The project has three content layers:

1. **Booklet** (`booklet_module1.md`) — comprehensive written learning guide
2. **Slides** (`Module_*/slides.md`, `Module_*/*.pdf`) — presentation slides (Marp format for .md)
3. **Demos** — two types:
   - **Jupyter notebooks** (`.ipynb`) show traditional workflow problems
   - **Marimo apps** (`.py`) demonstrate reactive solutions to those same problems

Marimo apps are pure Python files where each cell is a function decorated by marimo. Cells declare dependencies through function arguments, enabling automatic reactivity and enforced execution order.

## Key Marimo App Files

- `demo_mo.py` — minimal marimo app template
- `Module_1/1.3.py` — compound interest calculator with reactive UI sliders
- `Module_3/module_1_3_reactive_notebook.py` — ML classification demo (Random Forest with interactive noise/samples control)
