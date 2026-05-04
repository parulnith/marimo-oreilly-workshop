# marimo for AI and ML Development
*Enable reactive execution and predictable AI workflows*

*Sponsored by [marimo](https://marimo.io/)*

![Workshop banner](1775595001973.jpeg)

Workshop materials for the O'Reilly Live course **[marimo for AI and ML Development](https://learning.oreilly.com/live-events/marimo-for-ai-and-ml-development/0642572355555/)**.

The course introduces **marimo**, a next-generation Python programming environment for AI and ML, and shows how to build interactive, reproducible, and reusable workflows that improve on traditional notebook-based development.

## Workshop Modules

### [Module 1: Why Interactive Programming Environments Matter for AI and ML](Module_1/)
This module explores why interactive programming environments are at the very core of modern AI and ML development. We'll look at the shortcomings of traditional notebook systems and discover how modern execution models like marimo help you experiment faster and more reliably.

### [Module 2: Reproducibility as a Baseline for Trustworthy AI](Module_2/)
There's a big difference between just running your code again and reliably getting the same results across different computers and over time. This section will make that distinction clear.

### [Module 3: Why Interactivity Accelerates AI Discovery](Module_3/)
Interactivity is absolutely vital for truly understanding your data and your models in AI development.

### [Module 4: How to Use AI Coding Agents for AI/ML Development](Module_4/)
AI coding agents work best when they're integrated into your environment from the very beginning. This module provides practical advice for using modern AI assistance: when to trust it, what information it needs, and how to choose the best setup for your work.

### [Module 5: From Interactive Work to Reusable Systems](Module_5/)
This module shows you how to move beyond private experimentation and create something that others can easily run, inspect and build upon.

Each module has a `notes_*.md` file with the talking points for that section.

## How to Use This Repo

Clone the repo:

```bash
git clone <repository-url>
cd "Marimo Workshop"
```

### Option 1: Using pip (standard Python)

```bash
python -m venv .venv
source .venv/bin/activate     # on Windows: .venv\Scripts\activate
pip install marimo
marimo edit Module_1/1_2_marimo_reactive_workflow.py
```

Or launch the directory browser:

```bash
marimo edit .
```

### Option 2: Using uv (recommended)

[uv](https://docs.astral.sh/uv/) is faster and handles environments automatically:

```bash
uv sync
uv run marimo edit Module_1/1_2_marimo_reactive_workflow.py
```

The modules are progressive — start with Module 1 and work through them in order. Jupyter notebooks (`.ipynb`) in Modules 1 and 2 are intentionally included as the "before" baseline; the marimo `.py` files alongside them are the "after."

## Prerequisites

- Python 3.10+
- [marimo](https://marimo.io/) (installed via pip or uv as shown above)
- For Module 4: [Ollama](https://ollama.com/) installed locally — see [Module_4/Ollama-Setup.md](Module_4/Ollama-Setup.md)
